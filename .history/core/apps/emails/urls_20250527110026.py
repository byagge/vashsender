# core/apps/emails/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SenderEmailViewSet,EmailPlatformSpaView

router = DefaultRouter()
router.register(r'emails', SenderEmailViewSet, basename='sender-email')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', DomainsSpaView.as_view(), name='emails-spa'),
    path('confirm-sender/', SenderConfirmView.as_view(), name='confirm-sender'),
]
