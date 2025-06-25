# core/apps/emails/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomainViewSet, SenderEmailViewSet, EmailPlatformSpaView

router = DefaultRouter()
router.register(r'domains', DomainViewSet, basename='domain')
router.register(r'emails',  SenderEmailViewSet, basename='email')

urlpatterns = [
    # API
    path('api/', include(router.urls)),
    # Одна SPA-страница
    path('', EmailPlatformSpaView.as_view(), name='emails-spa'),
]
