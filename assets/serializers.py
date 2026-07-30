from rest_framework import serializers
from .models import AssetCategory, Asset, AssetSpec, AssetDocument, AssetEvent


class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'


class AssetSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetSpec
        fields = ['id', 'key', 'value']


class AssetDocumentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()

    class Meta:
        model = AssetDocument
        fields = ['id', 'asset', 'doc_type', 'file', 'url', 'filename', 'is_public', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['uploaded_by', 'uploaded_at', 'url', 'filename']

    def get_url(self, obj):
        return obj.file.url if obj.file else None

    def get_filename(self, obj):
        return obj.file.name.rsplit('/', 1)[-1] if obj.file else None

class AssetEventSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)

    class Meta:
        model = AssetEvent
        fields = ['id', 'event_type', 'performed_by_name', 'note', 'occurred_at']
        read_only_fields = fields  # append-only, never editable via API either


class AssetSerializer(serializers.ModelSerializer):
    specs = AssetSpecSerializer(many=True, read_only=True)
    documents = AssetDocumentSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    owning_department_name = serializers.CharField(source='owning_department.name', read_only=True)
    active_loan = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id', 'asset_tag', 'owning_department', 'created_at', 'updated_at']

    def get_active_loan(self, obj):
        loan = obj.loans.filter(status='active').first()
        if not loan:
            return None
        return {
            'id': loan.id,
            'to_department_name': loan.to_department.name,
            'expected_return': loan.expected_return,
        }

class AssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'asset_tag', 'name', 'category', 'owning_department', 'acquisition_type',
                  'condition_on_receipt', 'donor_name', 'vendor', 'purchase_date',
                  'cost', 'warranty_expiry', 'amc_expiry', 'amc_vendor_contact',
                  'current_location', 'notes']
        read_only_fields = ['id', 'asset_tag']
        extra_kwargs = {'owning_department': {'required': False}}