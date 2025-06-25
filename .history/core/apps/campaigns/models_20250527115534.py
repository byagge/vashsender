# core/apps/campaigns/models.py

import uuid
from django.db import models
from django.conf import settings

class Campaign(models.Model):
    """
    Рассылка (кампания).
    """
    STATUS_DRAFT     = 'draft'
    STATUS_SENDING   = 'sending'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_DRAFT,     'Черновик'),
        (STATUS_SENDING,   'Отправляется'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaigns')
    name           = models.CharField(max_length=255)
    template       = models.ForeignKey('mail_templates.EmailTemplate', on_delete=models.PROTECT)
    sender_email   = models.ForeignKey('emails.SenderEmail', on_delete=models.PROTECT)
    subject        = models.CharField(max_length=255)
    sender_name    = models.CharField(max_length=100, blank=True)
    reply_to       = models.EmailField(blank=True)
    contact_lists  = models.ManyToManyField('mailer.ContactList', related_name='campaigns')
    scheduled_at   = models.DateTimeField(null=True, blank=True)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    created_at     = models.DateTimeField(auto_now_add=True)
    sent_at        = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
