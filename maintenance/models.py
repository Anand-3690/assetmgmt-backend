from django.db import models


class MaintenanceRecord(models.Model):
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='maintenance_records')
    service_date = models.DateField()
    vendor = models.CharField(max_length=200, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    next_due = models.DateField(null=True, blank=True)


class NotificationLog(models.Model):
    ALERT_CHOICES = [
        ('warranty_expiring', 'Warranty Expiring'),
        ('amc_expiring', 'AMC Expiring'),
        ('loan_overdue', 'Loan Overdue'),
    ]
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='notifications')
    alert_type = models.CharField(max_length=30, choices=ALERT_CHOICES)
    period = models.CharField(max_length=7)  # "2026-07" — the dedupe bucket
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('asset', 'alert_type', 'period')
