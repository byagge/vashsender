# mailer_templates/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailTemplateViewSet, TemplateSpaView

router = DefaultRouter()
router.register(r'templates', EmailTemplateViewSet, basename='templates')

urlpatterns = [
    # DRF API endpoints: /api/templates/ , /api/templates/{id}/
    path('api/', include(router.urls)),

    # SPA view для редактирования/списка шаблонов
    path('', TemplateSpaView.as_view(), name='templates_spa'),
]
