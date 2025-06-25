# core/apps/emails/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomainViewSet, DomainsSpaView

router = DefaultRouter()
router.register(r'domains', DomainViewSet, basename='domain')

urlpatterns = [
    # API под /emails/domains/api/domains/
    path('domains/api/', include(router.urls)),

    # SPA-страница по /emails/domains/
    path('domains/', DomainsSpaView.as_view(), name='domains-spa'),
]
