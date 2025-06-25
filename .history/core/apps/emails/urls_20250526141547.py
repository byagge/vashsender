from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomainViewSet

router = DefaultRouter()
router.register(r'domains', DomainViewSet, basename='domain')

urlpatterns = [
    path('api/', include(router.urls)),
]
