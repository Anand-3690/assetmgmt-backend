from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserAdminForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserAdminForm
    fieldsets = UserAdmin.fieldsets + (
        ('Organization', {'fields': ('campus', 'department', 'role')}),
    )
    list_display = ('username', 'email', 'department', 'role', 'is_staff')
    list_filter = ('role', 'department')