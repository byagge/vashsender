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

class DomainViewSet(viewsets.ModelViewSet):
    """
    CRUD для Domains на /emails/domains/api/domains/
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
        POST /.../domains/{id}/verify/  
        Запускает проверку DNS записей (spf/dkim → is_verified).
        """
        domain = self.get_object()

        # Здесь интегрируйте реальную проверку DNS.
        # Для примера помечаем рандомно:
        domain.spf_verified  = random.choice([True, False])
        domain.dkim_verified = random.choice([True, False])
        domain.is_verified   = domain.spf_verified and domain.dkim_verified
        domain.save(update_fields=['spf_verified','dkim_verified','is_verified'])

        return Response({
            'spf_verified':  domain.spf_verified,
            'dkim_verified': domain.dkim_verified,
            'is_verified':   domain.is_verified,
        })

class DomainsSpaView(LoginRequiredMixin, TemplateView):
    template_name = 'emails/domains.html'
