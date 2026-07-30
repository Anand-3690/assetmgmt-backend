# loans/serializers.py
from rest_framework import serializers
from .models import AssetLoan


class AssetLoanSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    asset_tag = serializers.CharField(source='asset.asset_tag', read_only=True)
    to_department_name = serializers.CharField(source='to_department.name', read_only=True)

    class Meta:
        model = AssetLoan
        fields = '__all__'
        read_only_fields = ['sent_date', 'sent_by']