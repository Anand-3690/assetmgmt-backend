from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Organization', {'fields': ('department', 'role')}),
    )
    list_display = ('username', 'email', 'department', 'role', 'is_staff')
    list_filter = ('role', 'department')