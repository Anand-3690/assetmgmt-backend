from rest_framework import serializers
from .models import User


class MeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'department', 'department_name', 'must_change_password']