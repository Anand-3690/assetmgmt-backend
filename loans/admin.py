from django.contrib import admin
from .models import AssetLoan


@admin.register(AssetLoan)
class AssetLoanAdmin(admin.ModelAdmin):
    list_display = ('asset', 'to_department', 'sent_date', 'expected_return', 'status')
    list_filter = ('status', 'to_department')