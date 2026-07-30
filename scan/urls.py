from django.urls import path
from . import views

urlpatterns = [
    path('a/<str:asset_tag>/', views.asset_detail, name='asset_detail'),
    path('a/<str:asset_tag>/qr/', views.asset_qr, name='asset_qr'),
    path('a/<str:asset_tag>/label/', views.asset_label, name='asset_label'),
]