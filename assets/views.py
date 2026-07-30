from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from .serializers import AssetSerializer, AssetCreateSerializer
from accounts.permissions import IsDeptAdminOrOrgAdmin, IsSameDepartmentObject
from .models import Asset, AssetCategory, AssetEvent
from .serializers import AssetSerializer, AssetCategorySerializer
from .querysets import DepartmentScopedViewSetMixin
from .models import AssetDocument
from .serializers import AssetDocumentSerializer

class AssetDocumentViewSet(viewsets.ModelViewSet):
    queryset = AssetDocument.objects.all()
    serializer_class = AssetDocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'org_admin':
            return AssetDocument.objects.all()
        return AssetDocument.objects.filter(asset__owning_department=user.department)

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            return [IsAuthenticated(), IsDeptAdminOrOrgAdmin()]
        return [IsAuthenticated()]

    def _check_department(self, asset):
        user = self.request.user
        if user.role != 'org_admin' and asset.owning_department_id != user.department_id:
            raise PermissionDenied("Cannot manage documents for another department's asset.")

    def perform_create(self, serializer):
        asset = serializer.validated_data['asset']
        self._check_department(asset)
        serializer.save(uploaded_by=self.request.user)

    def perform_destroy(self, instance):
        self._check_department(instance.asset)
        instance.delete()

class AssetCategoryViewSet(viewsets.ModelViewSet):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]


class AssetViewSet(DepartmentScopedViewSetMixin, viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get_serializer_class(self):
        return AssetCreateSerializer if self.action == 'create' else AssetSerializer
    
    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsDeptAdminOrOrgAdmin(), IsSameDepartmentObject()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'org_admin':
            if not serializer.validated_data.get('owning_department'):
                raise ValidationError({'owning_department': 'Required when creating as org admin.'})
            asset = serializer.save()
        else:
            asset = serializer.save(owning_department=user.department)
        AssetEvent.objects.create(asset=asset, event_type='created', performed_by=user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsSameDepartmentObject])
    def flag_missing(self, request, pk=None):
        asset = self.get_object()
        asset.status = 'missing'
        asset.save(update_fields=['status'])
        AssetEvent.objects.create(
            asset=asset, event_type='flagged_missing',
            performed_by=request.user, note=request.data.get('note', ''),
        )
        return Response(AssetSerializer(asset).data)