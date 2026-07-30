from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from assets.models import Asset
from loans.models import AssetLoan
from maintenance.models import NotificationLog
from accounts.models import User

THRESHOLDS = [30, 7, 1]  # days before expiry to warn at


class Command(BaseCommand):
    help = 'Checks warranty/AMC expiry and loan due dates, sends alert emails.'

    def handle(self, *args, **options):
        today = date.today()
        period = today.strftime('%Y-%m')

        self._check_expiry(today, period, field='warranty_expiry', alert_type='warranty_expiring')
        self._check_expiry(today, period, field='amc_expiry', alert_type='amc_expiring')
        self._check_overdue_loans(today, period)

    def _check_expiry(self, today, period, field, alert_type):
        for days_out in THRESHOLDS:
            target_date = today + timedelta(days=days_out)
            assets = Asset.objects.exclude(status='retired').filter(**{field: target_date})
            for asset in assets:
                self._notify(asset, alert_type, period,
                             subject=f"{asset.name} ({asset.asset_tag}) — {field.replace('_', ' ')} in {days_out} days",
                             body=f"{asset.name}, tagged {asset.asset_tag}, owned by {asset.owning_department}, "
                                  f"has {field.replace('_', ' ')} on {getattr(asset, field)}.")

    def _check_overdue_loans(self, today, period):
        overdue = AssetLoan.objects.filter(status='active', expected_return__lt=today)
        for loan in overdue:
            loan.status = 'overdue'
            loan.save(update_fields=['status'])
            asset = loan.asset
            self._notify(asset, 'loan_overdue', period,
                         subject=f"{asset.name} ({asset.asset_tag}) — loan overdue",
                         body=f"{asset.name} was loaned to {loan.to_department} and was due back "
                              f"on {loan.expected_return}. It has not been marked returned.",
                         extra_departments=[loan.to_department])

    def _notify(self, asset, alert_type, period, subject, body, extra_departments=None):
        try:
            NotificationLog.objects.create(asset=asset, alert_type=alert_type, period=period)
        except IntegrityError:
            return  # already sent this alert for this asset this month — dedupe

        departments = [asset.owning_department] + (extra_departments or [])
        recipients = list(
            User.objects.filter(department__in=departments, role__in=['dept_admin', 'org_admin'])
            .exclude(email='')
            .values_list('email', flat=True)
        )
        recipients += list(
            User.objects.filter(role='org_admin').exclude(email='').values_list('email', flat=True)
        )
        recipients = list(set(recipients))

        if recipients:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=False)
            self.stdout.write(f"Sent {alert_type} for {asset.asset_tag} to {len(recipients)} recipient(s)")