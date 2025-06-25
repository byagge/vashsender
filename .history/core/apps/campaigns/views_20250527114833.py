# core/apps/campaigns/views.py

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Campaign
from .serializers import CampaignSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    """
    CRUD + отправка рассылки.
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
            return Response({'detail': 'Кампанию нельзя отправить повторно.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Сразу ставим статус «sending»
        campaign.status = Campaign.STATUS_SENDING
        campaign.save(update_fields=['status'])

        # Здесь вы можете поставить задачу в Celery:
        # send_campaign_task.delay(str(campaign.id))
        # или выполнить синхронно:
        self._send_sync(campaign)

        return Response({'detail': 'Кампанию запущено.'})

    def _send_sync(self, campaign: Campaign):
        """
        Простейшая отправка без очередей.
        Пробегаем по контактам и кидаем письмо.
        """
        from django.core.mail import EmailMultiAlternatives
        # собираем всех контактов
        qs = campaign.contact_lists.prefetch_related('contacts__email_addresses')
        recipients = set()
        for clist in qs:
            for contact in clist.contacts.all():
                # допустим, контакт хранит email в поле `email`
                recipients.add(contact.email)

        # собираем содержимое из шаблона
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

        # обновляем статус
        campaign.status = Campaign.STATUS_COMPLETED
        campaign.sent_at = timezone.now()
        campaign.save(update_fields=['status', 'sent_at'])


class CampaignsSpaView(LoginRequiredMixin, TemplateView):
    """
    Отдаёт один HTML-шаблон, внутри которого уже SPA на Alpine.js.
    """
    template_name = 'campaigns.html'