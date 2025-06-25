# core/apps/mail_templates/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailTemplateViewSet, TemplateSpaView

router = DefaultRouter()
router.register(r'api/templates', EmailTemplateViewSet, basename='templates')

urlpatterns = [
    path('', TemplateSpaView.as_view(), name='spa'),
    path('', include(router.urls)),
]
