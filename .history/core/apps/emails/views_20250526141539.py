# emails/views.py
import dns.resolver
import secrets

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Domain
from .serializers import DomainSerializer

class DomainViewSet(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Domain.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        token = secrets.token_urlsafe(16)
        serializer.save(owner=self.request.user, verification_token=token)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        POST /emails/domains/api/domains/{pk}/verify/
        Проверяем TXT-записи для SPF и DKIM.
        """
        domain = self.get_object()
        name = domain.domain_name

        spf_ok = False
        dkim_ok = False
        # 1) SPF: ищем TXT с v=spf1
        try:
            answers = dns.resolver.resolve(name, 'TXT')
            for r in answers:
                txt = r.to_text().strip('"')
                if txt.lower().startswith('v=spf1'):
                    spf_ok = True
                    break
        except Exception:
            spf_ok = False

        # 2) DKIM: предполагаем селектор = verification_token
        selector = domain.verification_token
        try:
            dkim_name = f"{selector}._domainkey.{name}"
            answers = dns.resolver.resolve(dkim_name, 'TXT')
            for r in answers:
                txt = r.to_text().strip('"')
                if txt.lower().startswith('v=dkim1;'):
                    dkim_ok = True
                    break
        except Exception:
            dkim_ok = False

        # 3) Если оба прошли — считаем домен верифицированным
        domain.spf_verified  = spf_ok
        domain.dkim_verified = dkim_ok
        domain.is_verified   = spf_ok and dkim_ok
        domain.save(update_fields=['spf_verified','dkim_verified','is_verified'])

        ser = DomainSerializer(domain)
        return Response(ser.data, status=status.HTTP_200_OK)
