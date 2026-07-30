from django.db import models
from django.conf import settings


class AssetLoan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='loans')
    to_department = models.ForeignKey('campuses.Department', on_delete=models.PROTECT, related_name='incoming_loans')
    sent_date = models.DateField(auto_now_add=True)
    expected_return = models.DateField()
    actual_return = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)