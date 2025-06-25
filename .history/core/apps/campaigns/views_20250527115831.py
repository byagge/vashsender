from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives

from .models import Campaign
from .serializers import CampaignSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    """
    CRUD + экшен send для рассылки.
    """
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='send')
    def send(self, request, pk=None):
        campaign = self.get_object()
        if campaign.status != Campaign.STATUS_DRAFT:
            return Response(
                {'detail': 'Кампанию можно отправить только из статуса «черновик».'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # переключаем статус
        campaign.status = Campaign.STATUS_SENDING
        campaign.save(update_fields=['status'])

        # синхронная отправка (в продакшене лучше Celery)
        self._send_sync(campaign)
        return Response({'detail': 'Кампанию запущено.'})

    def _send_sync(self, campaign: Campaign):
        # собираем получателей
        recipients = set()
        for cl in campaign.contact_lists.all():
            for contact in cl.contacts.all():
                recipients.add(contact.email)

        subject = campaign.subject
        from_email = f"{campaign.sender_name} <{campaign.sender_email.email}>"
        html_content = campaign.template.html_content
        text_content = campaign.template.plain_text_content or ''

        for to in recipients:
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to],
                reply_to=[campaign.reply_to] if campaign.reply_to else None
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        # завершаем кампанию
        campaign.status = Campaign.STATUS_COMPLETED
        campaign.sent_at = timezone.now()
        campaign.save(update_fields=['status', 'sent_at'])


class CampaignsSpaView(LoginRequiredMixin, TemplateView):
    """
    Отдаёт один HTML-шаблон, внутри которого уже SPA на Alpine.js.
    """
    template_name = 'campaigns.html'
