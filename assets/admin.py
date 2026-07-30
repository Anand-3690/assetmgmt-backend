from django.contrib import admin
from .models import AssetCategory, Asset, AssetSpec, AssetDocument, AssetEvent


class AssetSpecInline(admin.TabularInline):
    model = AssetSpec
    extra = 1


class AssetDocumentInline(admin.TabularInline):
    model = AssetDocument
    extra = 1


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'name', 'owning_department', 'status', 'acquisition_type')
    list_filter = ('status', 'acquisition_type', 'owning_department', 'category')
    search_fields = ('asset_tag', 'name')
    readonly_fields = ('asset_tag', 'created_at', 'updated_at')
    inlines = [AssetSpecInline, AssetDocumentInline]


@admin.register(AssetEvent)
class AssetEventAdmin(admin.ModelAdmin):
    list_display = ('asset', 'event_type', 'performed_by', 'occurred_at')
    list_filter = ('event_type',)
    readonly_fields = [f.name for f in AssetEvent._meta.fields]  # append-only — no editing via admin

    def has_change_permission(self, request, obj=None):
        return False