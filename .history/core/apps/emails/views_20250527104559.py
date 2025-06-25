# core/apps/emails/views.py

import uuid
import dns.resolver
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Domain, SenderEmail
from .serializers import DomainSerializer, SenderEmailSerializer

class DomainViewSet(viewsets.ModelViewSet):
    serializer_class    = DomainSerializer
    permission_classes  = [IsAuthenticated]

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
                b''.join(r.strings).decode('utf-8', errors='ignore').lower().startswith('v=spf1')
                for r in answers
            )
        except Exception:
            spf_ok = False
        # DKIM (selector ep1)
        try:
            lookup = f"ep1._domainkey.{domain.domain_name}"
            answers = dns.resolver.resolve(lookup, 'TXT')
            dkim_ok = any(
                b''.join(r.strings).decode('utf-8', errors='ignore').startswith('v=DKIM1')
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
    serializer_class    = SenderEmailSerializer
    permission_classes  = [IsAuthenticated]

    def get_queryset(self):
        return SenderEmail.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # можно тут сразу отправить verification email
        serializer.save(owner=self.request.user)


class DomainsSpaView(LoginRequiredMixin, TemplateView):
    template_name = 'domains.html'