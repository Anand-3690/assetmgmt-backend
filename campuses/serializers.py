from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'campus', 'campus_name']