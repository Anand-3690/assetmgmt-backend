# loans/serializers.py
from rest_framework import serializers

from django.db import models as db_models
from .models import AssetLoan


class AssetLoanSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    asset_tag = serializers.CharField(source='asset.asset_tag', read_only=True)
    to_department_name = serializers.CharField(source='to_department.name', read_only=True)

    class Meta:
        model = AssetLoan
        fields = '__all__'
        read_only_fields = ['sent_date', 'sent_by']

    def validate(self, data):
        asset = data.get('asset') or (self.instance.asset if self.instance else None)
        if asset is None:
            return data
        requested = data.get('quantity', self.instance.quantity if self.instance else 1)
        loaned = asset.loans.filter(status='active').exclude(pk=self.instance.pk if self.instance else None).aggregate(
            total=db_models.Sum('quantity'))['total'] or 0
        available = asset.quantity - loaned
        if requested > available:
            raise serializers.ValidationError(f"Only {available} available to loan.")
        return data