# core/apps/mail_templates/views.py

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EmailTemplate
from .serializers import EmailTemplateSerializer

class EmailTemplateViewSet(viewsets.ModelViewSet):
    """
    CRUD для EmailTemplate
    """
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Показываем только шаблоны текущего пользователя
        return EmailTemplate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # При создании автоматически привязываем к пользователю
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Переопределяем, чтобы отлавливать integrity errors на уникальность названия
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"detail": "Шаблон с таким названием уже существует."},
                status=status.HTTP_400_BAD_REQUEST
            )

class TemplateSpaView(LoginRequiredMixin, TemplateView):
    """
    Одиночная точка входа SPA — выдаёт HTML с Alpine.js и готовым <script>.
    """
    template_name = "mail_templates/index.html"
