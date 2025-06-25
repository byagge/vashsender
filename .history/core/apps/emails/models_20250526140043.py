# core/apps/emails/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid

class Domain(models.Model):
    """
    Отправляющие домены пользователя.
    """
    owner              = models.ForeignKey(
                              settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='domains'
                          )
    domain_name        = models.CharField(
                              max_length=253,
                              help_text="Например: example.com"
                          )
    is_verified        = models.BooleanField(
                              default=False,
                              help_text="Общий флаг: все DNS-записи пройдены"
                          )
    dkim_verified      = models.BooleanField(
                              default=False,
                              help_text="DKIM TXT-запись пройдена"
                          )
    spf_verified       = models.BooleanField(
                              default=False,
                              help_text="SPF TXT-запись пройдена"
                          )
    verification_token = models.CharField(
                              max_length=64,
                              unique=True,
                              help_text="Уникальный токен для DNS-подтверждения"
                          )
    created_at         = models.DateTimeField(
                              auto_now_add=True
                          )

    class Meta:
        unique_together = ('owner','domain_name')
        ordering = ['-created_at']
        verbose_name = "Домен"
        verbose_name_plural = "Домены"

    def save(self, *args, **kwargs):
        # при создании генерим токен
        if not self.verification_token:
            self.verification_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.domain_name} ({'✔' if self.is_verified else '✘'})"


class SenderEmail(models.Model):
    """
    Разрешенные отправляющие адреса в рамках доменов.
    """
    owner              = models.ForeignKey(
                              settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='sender_emails'
                          )
    email              = models.EmailField(
                              unique=True,
                              help_text="Например: user@example.com"
                          )
    domain             = models.ForeignKey(
                              Domain,
                              on_delete=models.CASCADE,
                              related_name='sender_emails'
                          )
    is_verified        = models.BooleanField(
                              default=False,
                              help_text="Подтвержден ли адрес (click-письмо)"
                          )
    verification_token = models.CharField(
                              max_length=64,
                              unique=True,
                              help_text="Уникальный токен для подтверждения email"
                          )
    created_at         = models.DateTimeField(
                              auto_now_add=True
                          )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sender Email"
        verbose_name_plural = "Sender Emails"

    def save(self, *args, **kwargs):
        if not self.verification_token:
            self.verification_token = uuid.uuid4().hex[:16]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({'✔' if self.is_verified else '✘'})"
