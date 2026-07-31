import uuid
from django.db import models
from django.conf import settings

from assets.querysets import DepartmentScopedQuerySet


class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g. "MCH" for Machine, used in asset_tag

    class Meta:
        verbose_name_plural = "Asset categories"

    def __str__(self):
        return self.name


class Asset(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('under_maintenance', 'Under Maintenance'),
        ('missing', 'Missing'),
        ('retired', 'Retired'),
    ]
    ACQUISITION_CHOICES = [
        ('purchased', 'Purchased'),
        ('donated', 'Donated'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('unknown', 'Unknown'),
    ]

    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=20, blank=True)  # "pcs", "kg", "" for single items

    objects = DepartmentScopedQuerySet.as_manager()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_tag = models.CharField(max_length=30, unique=True, editable=False, db_index=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, related_name='assets')
    owning_department = models.ForeignKey('campuses.Department', on_delete=models.PROTECT, related_name='assets')
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_assets')
    current_location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    acquisition_type = models.CharField(max_length=20, choices=ACQUISITION_CHOICES)
    condition_on_receipt = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True)
    donor_name = models.CharField(max_length=200, blank=True)

    vendor = models.CharField(max_length=200, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    amc_expiry = models.DateField(null=True, blank=True)
    amc_vendor_contact = models.CharField(max_length=200, blank=True)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.asset_tag:
            self.asset_tag = self._generate_asset_tag()
        super().save(*args, **kwargs)

    def _generate_asset_tag(self):
        dept_code = self.owning_department.name[:3].upper()
        cat_code = self.category.code.upper()
        prefix = f"{dept_code}-{cat_code}-"
        last = Asset.objects.filter(asset_tag__startswith=prefix).order_by('-asset_tag').first()
        next_num = int(last.asset_tag.split('-')[-1]) + 1 if last else 1
        return f"{prefix}{next_num:04d}"

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"


class AssetSpec(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='specs')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    class Meta:
        unique_together = ('asset', 'key')


class AssetDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('manual', 'Manual'),
        ('warranty_card', 'Warranty Card'),
        ('invoice', 'Invoice'),
        ('amc_contract', 'AMC Contract'),
        ('photo', 'Photo'),
    ]
    PUBLIC_DEFAULTS = {'manual', 'photo'}

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    file = models.FileField(upload_to='documents/')
    is_public = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None and not self.is_public and self.doc_type in self.PUBLIC_DEFAULTS:
            self.is_public = True
        super().save(*args, **kwargs)


class AssetEvent(models.Model):
    EVENT_CHOICES = [
        ('created', 'Created'),
        ('relocated', 'Relocated'),
        ('status_changed', 'Status Changed'),
        ('retired', 'Retired'),
        ('flagged_missing', 'Flagged Missing'),
        ('quantity_adjusted', 'Quantity Adjusted'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)