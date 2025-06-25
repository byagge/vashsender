# core/apps/emails/views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.generic import TemplateView

from .models import Domain, SenderEmail
from .serializers import DomainSerializer, SenderEmailSerializer


class DomainViewSet(viewsets.ModelViewSet):
    """
    CRUD для доменов пользователя.
    Дополнительно:
      - POST /domains/{pk}/verify/ — запускает проверку DNS (специфичная бизнес-логика)
    """
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Domain.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Дополнительная ручка: после настройки DNS клиент нажимает «Check DNS»,
        и мы перепроверяем записи (например real logic там, здесь просто пример).
        """
        domain = self.get_object()

        # TODO: сюда свою логику проверки DNS (spf, dkim)  
        # Ниже — упрощённый пример «рандомной верификации»
        import random
        domain.spf_verified   = random.choice([True, False])
        domain.dkim_verified  = random.choice([True, False])
        domain.is_verified    = domain.spf_verified and domain.dkim_verified
        domain.save(update_fields=['spf_verified', 'dkim_verified', 'is_verified'])

        return Response({
            'spf_verified': domain.spf_verified,
            'dkim_verified': domain.dkim_verified,
            'is_verified': domain.is_verified,
        })


class SenderEmailViewSet(viewsets.ModelViewSet):
    """
    CRUD для sender-emails.
    """
    serializer_class = SenderEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SenderEmail.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        """
        Отправить повторное письмо верификации.
        """
        sender = self.get_object()
        # тут должна быть логика отправки письма
        # send_verification_email(sender.email, sender.verification_token)
        return Response({'detail': f'Verification email sent to {sender.email}'}, status=status.HTTP_200_OK)
