# loans/views.py

from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models as db_models

from accounts.permissions import IsDeptAdminOrOrgAdmin
from .models import AssetLoan
from .serializers import AssetLoanSerializer


class AssetLoanViewSet(viewsets.ModelViewSet):
    queryset = AssetLoan.objects.all()
    serializer_class = AssetLoanSerializer
    permission_classes = [IsAuthenticated, IsDeptAdminOrOrgAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'org_admin':
            return AssetLoan.objects.all()
        return AssetLoan.objects.filter(
            Q(asset__owning_department=user.department) | Q(to_department=user.department)
        )

    def perform_create(self, serializer):
        serializer.save(sent_by=self.request.user)

    # loans/views.py
    @action(detail=False)
    def dashboard(self, request):
        user = request.user
        qs = self.get_queryset().filter(status='active')

        if user.role == 'org_admin':
            return Response({
                'sent': AssetLoanSerializer(qs, many=True).data,
                'received': [],
            })

        dept = user.department
        return Response({
            'sent': AssetLoanSerializer(qs.filter(asset__owning_department=dept), many=True).data,
            'received': AssetLoanSerializer(qs.filter(to_department=dept), many=True).data,
        })

    @action(detail=False)
    def history(self, request):
        qs = self.get_queryset().exclude(status='active').order_by('-sent_date')
        return Response(AssetLoanSerializer(qs, many=True).data)