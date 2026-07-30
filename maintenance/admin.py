from django.contrib import admin
from .models import MaintenanceRecord, NotificationLog


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('asset', 'service_date', 'vendor', 'next_due')
    list_filter = ('vendor',)


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('asset', 'alert_type', 'period', 'sent_at')
    readonly_fields = [f.name for f in NotificationLog._meta.fields]

    def has_add_permission(self, request):
        return False  # this table is only ever written by the alert cron, never by hand