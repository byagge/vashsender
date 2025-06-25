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
    try:
        answers = dns.resolver.resolve(domain_name, 'TXT')
        for r in answers:
            txt = r.to_text().strip('"')
            if txt.startswith('v=spf1'):
                return True
    except Exception:
        pass
    return False

def has_dkim(domain_name: str, selector: str = 'ep1') -> bool:
    try:
        dkim_domain = f"{selector}._domainkey.{domain_name}"
        answers = dns.resolver.resolve(dkim_domain, 'TXT')
        for r in answers:
            txt = r.to_text().strip('"')
            if txt.startswith('v=DKIM1'):
                return True
    except Exception:
        pass
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
        """
        POST /emails/domains/api/domains/{pk}/verify/
        Перепроверить SPF и DKIM, обновить поля и вернуть их в ответе.
        """
        domain = self.get_object()
        domain.spf_verified = has_spf(domain.domain_name)
        domain.dkim_verified = has_dkim(domain.domain_name, selector='ep1')
        domain.is_verified = domain.spf_verified and domain.dkim_verified
        domain.save(update_fields=['spf_verified', 'dkim_verified', 'is_verified'])
        ser = self.get_serializer(domain)
        return Response(ser.data, status=status.HTTP_200_OK)

class DomainsSpaView(LoginRequiredMixin, TemplateView):
    template_name = 'domains.html'
