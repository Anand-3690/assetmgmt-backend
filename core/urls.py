"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from assets.views import AssetDocumentViewSet

from assets.views import AssetViewSet, AssetCategoryViewSet
from loans.views import AssetLoanViewSet
from accounts.views import me
from campuses.views import DepartmentViewSet

router = DefaultRouter()
router.register('assets', AssetViewSet, basename='asset')
router.register('asset-categories', AssetCategoryViewSet, basename='assetcategory')
router.register('loans', AssetLoanViewSet, basename='assetloan')
router.register('departments', DepartmentViewSet, basename='department')
router.register('asset-documents', AssetDocumentViewSet, basename='assetdocument')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('scan.urls')),
    path('api/me/', me, name='me'),
]
