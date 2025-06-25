# core/apps/campaigns/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet

router = DefaultRouter()
router.register('campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('api/', include(router.urls)),
]
    