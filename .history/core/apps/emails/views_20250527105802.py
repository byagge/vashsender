# core/apps/emails/views.py

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import uuid
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import SenderEmail, Domain
from .serializers import SenderEmailSerializer

import uuid
import dns.resolver

from .models import Domain, SenderEmail
from .serializers import DomainSerializer, SenderEmailSerializer

class DomainViewSet(viewsets.ModelViewSet):
    serializer_class   = DomainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Domain.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        token = uuid.uuid4().hex
        serializer.save(owner=self.request.user, verification_token=token)

    @action(detail=True, methods=['post'], url_path='verify')
    def verify(self, request, pk=None):
        domain = self.get_object()
        # SPF
        try:
            answers = dns.resolver.resolve(domain.domain_name, 'TXT')
            spf_ok = any(
                b''.join(r.strings).decode().lower().startswith('v=spf1')
                for r in answers
            )
        except Exception:
            spf_ok = False
        # DKIM
        try:
            lookup = f"ep1._domainkey.{domain.domain_name}"
            answers = dns.resolver.resolve(lookup, 'TXT')
            dkim_ok = any(
                b''.join(r.strings).decode().startswith('v=DKIM1')
                for r in answers
            )
        except Exception:
            dkim_ok = False

        domain.spf_verified  = spf_ok
        domain.dkim_verified = dkim_ok
        domain.is_verified   = spf_ok and dkim_ok
        domain.save(update_fields=['spf_verified','dkim_verified','is_verified'])
        return Response(DomainSerializer(domain).data)


class SenderEmailViewSet(viewsets.ModelViewSet):
    """
    Создаём отправителя (sender email) со следующей логикой:
     - из email вытягиваем домен
     - проверяем, что Domain с таким name есть у пользователя
     - если нет — 400 с подсказкой добавить домен
     - если есть, но не подтверждён — 400 с подсказкой подтвердить домен
     - иначе создаём запись SenderEmail, генерируем токен и шлём письмо-подтверждение
    """
    serializer_class = SenderEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SenderEmail.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        email_addr = request.data.get('email', '').strip().lower()
        if '@' not in email_addr:
            return Response({'email': 'Неверный формат email.'},
                            status=status.HTTP_400_BAD_REQUEST)

        domain_part = email_addr.split('@', 1)[1]
        # 1) Домен должен существовать и принадлежать текущему пользователю
        try:
            domain_obj = Domain.objects.get(owner=request.user,
                                            domain_name=domain_part)
        except Domain.DoesNotExist:
            return Response(
                {'detail': f'Домен {domain_part} не найден. Сначала добавьте и подтвердите домен.'},
                status=status.HTTP_400_BAD_REQUEST)

        # 2) Домен должен быть верифицирован
        if not domain_obj.is_verified:
            return Response(
                {'detail': f'Домен {domain_part} ещё не подтверждён. Перейдите в раздел «Домены» и завершите верификацию.'},
                status=status.HTTP_400_BAD_REQUEST)

        # 3) Всё ок — создаём отправителя и шлём письмо
        token = uuid.uuid4().hex
        sender = SenderEmail.objects.create(
            owner=request.user,
            email=email_addr,
            domain=domain_obj,
            verification_token=token
        )

        # Отправляем письмо-подтверждение
        confirm_url = request.build_absolute_uri(
            f"/emails/confirm-sender/?token={token}"
        )
        send_mail(
            subject="Подтверждение отправителя",
            message=f"Пожалуйста, подтвердите ваш адрес: {confirm_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_addr],
            fail_silently=False,
        )

        return Response(
            {'detail': 'Письмо с подтверждением отправлено. Проверьте ваш почтовый ящик.'},
            status=status.HTTP_201_CREATED
        )


class EmailPlatformSpaView(LoginRequiredMixin, TemplateView):
    """
    Единая SPA-страница, где через Alpine.js переключаются 
    табы Emails ↔ Domains
    """
    template_name = 'domains.html'
