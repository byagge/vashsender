from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CampaignViewSet, CampaignsSpaView

router = DefaultRouter()
router.register('campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    # REST API
    path('api/', include(router.urls)),

    # SPA сама подхватывает Alpine.js и дергает этот же API
    path('', CampaignsSpaView.as_view(), name='campaigns_spa'),
]
