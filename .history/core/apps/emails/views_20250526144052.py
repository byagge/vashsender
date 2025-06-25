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

# apps/emails/dns_utils.py

import dns.resolver

def has_spf(domain_name: str) -> bool:
    """
    Ищем ровно ту TXT-запись, которая начинается с 'v=spf1'.
    """
    try:
        answers = dns.resolver.resolve(domain_name, 'TXT')
    except Exception:
        return False

    for rdata in answers:
        txt = b''.join(rdata.strings).decode('utf-8', errors='ignore')
        if txt.lower().startswith('v=spf1'):
            return True
    return False

def has_dkim(domain_name: str, selector: str = 'ep1') -> bool:
    """
    Делает запрос SELECTOR._domainkey.DOMAIN на TXT и проверяет, что запись начинается с 'v=DKIM1'.
    """
    lookup = f"{selector}._domainkey.{domain_name}"
    try:
        answers = dns.resolver.resolve(lookup, 'TXT')
    except Exception:
        return False

    for rdata in answers:
        txt = b''.join(rdata.strings).decode('utf-8', errors='ignore')
        if txt.startswith('v=DKIM1'):
            return True
    return False

# apps/emails/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Domain
from .serializers import DomainSerializer

# core/apps/emails/views.py

import uuid
import dns.resolver
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Domain
from .serializers import DomainSerializer

class DomainViewSet(viewsets.ModelViewSet):
    """
    CRUD для Domain + action verify для реальной DNS-проверки SPF/DKIM.
    """
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Domain.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # генерим токен тут
        token = uuid.uuid4().hex
        serializer.save(owner=self.request.user, verification_token=token)

    @action(detail=True, methods=['post'], url_path='verify')
    def verify(self, request, pk=None):
        """
        POST /emails/domains/api/domains/{pk}/verify/
        Проверяет реальные DNS-записи SPF и DKIM, обновляет поля.
        """
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

        # DKIM (используем селектор "ep1")
        try:
            selector = 'ep1'
            lookup = f"{selector}._domainkey.{domain.domain_name}"
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

        return Response(self.get_serializer(domain).data)


class DomainsSpaView(LoginRequiredMixin, TemplateView):
    template_name = 'domains.html'
