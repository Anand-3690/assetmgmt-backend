from django.contrib import admin
from .models import Campus, Department


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus')
    list_filter = ('campus',)
    search_fields = ('name',)
