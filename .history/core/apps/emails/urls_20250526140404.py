# core/apps/emails/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomainViewSet, SenderEmailViewSet, TemplateSpaView

router = DefaultRouter()
router.register(r'domains', DomainViewSet, basename='domain')
router.register(r'sender-emails', SenderEmailViewSet, basename='senderemail')

urlpatterns = [
    # API
    path('api/', include(router.urls)),

    # SPA-view
    path('', TemplateSpaView.as_view(), name='emails-spa'),
]
