# core/apps/emails/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Domain
from .serializers import DomainSerializer

import random

import dns.resolver

# emails/views.py
import dns.resolver
import secrets

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import uuid

from .models import Domain
from .serializers import DomainSerializer

# core/apps/emails/views.py
import uuid
import dns.resolver
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Domain
from .serializers import DomainSerializer

def has_spf(domain_name: str) -> bool:
    """
    Проверяем, есть ли на корне домена TXT-запись, начинающаяся с 'v=spf1'
    """
    try:
        answers = dns.resolver.resolve(domain_name, 'TXT')
    except Exception:
        return False

    for rdata in answers:
        # rdata.strings — список байтовых фрагментов
        try:
            txt = b''.join(rdata.strings).decode('utf-8')
        except Exception:
            # fallback, если строка в необычном формате
            txt = rdata.to_text().strip('"')
        if txt.lower().startswith('v=spf1'):
            return True

    return False

def has_dkim(domain_name: str, selector: str = 'ep1') -> bool:
    """
    Проверяем DNS-запись selector._domainkey.DOMAIN, что она начинается с 'v=DKIM1'
    """
    lookup = f"{selector}._domainkey.{domain_name}"
    try:
        answers = dns.resolver.resolve(lookup, 'TXT')
    except Exception:
        return False

    for rdata in answers:
        try:
            txt = b''.join(rdata.strings).decode('utf-8')
        except Exception:
            txt = rdata.to_text().strip('"')
        if txt.startswith('v=DKIM1'):
            return True

    return False

class DomainViewSet(viewsets.ModelViewSet):
    """
    CRUD для sender-доменов + проверка DNS (SPF/DKIM).
    """
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Domain.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # verification_token не передаем — сгенерируется по default в модели
        serializer.save(owner=self.request.user)

        @action(detail=True, methods=['post'], url_path='verify')
    def verify(self, request, pk=None):
        domain = self.get_object()
        domain.spf_verified  = has_spf(domain.domain_name)
        domain.dkim_verified = has_dkim(domain.domain_name)
        domain.is_verified   = domain.spf_verified and domain.dkim_verified
        domain.save(update_fields=['spf_verified','dkim_verified','is_verified'])
        return Response(self.get_serializer(domain).data)


class DomainsSpaView(LoginRequiredMixin, TemplateView):
    template_name = 'domains.html'
