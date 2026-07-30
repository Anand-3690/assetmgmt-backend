# loans/views.py
from xml.dom import ValidationErr

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
        asset = serializer.validated_data['asset']
        if asset.loans.filter(status='active').exists():
            raise ValidationErr('This asset is already on an active loan.')
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