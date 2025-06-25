# mailer_templates/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone

class EmailTemplate(models.Model):
    """
    Шаблон письма:
      - id                  — автоматически PK
      - owner               — владелец шаблона (пользователь)
      - title               — название шаблона
      - html_content        — HTML-контент (для рендеринга)
      - ck_content          — оригинальный контент CKEditor (если нужно хранить отдельно)
      - plain_text_content  — текстовая версия письма
      - is_draft            — флаг черновика
      - send_count          — сколько раз отправлялся
      - created_at, updated_at — метки времени
    """
    owner               = models.ForeignKey(
                              settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='email_templates'
                          )
    title               = models.CharField(
                              max_length=200,
                              help_text="Название шаблона"
                          )
    html_content        = models.TextField(
                              help_text="HTML-контент, используется для рендеринга письма"
                          )
    ck_content          = models.TextField(
                              blank=True,
                              help_text="Исходный контент из CKEditor (если нужен отдельно)"
                          )
    plain_text_content  = models.TextField(
                              blank=True,
                              help_text="Текстовая версия письма без HTML"
                          )
    is_draft            = models.BooleanField(
                              default=True,
                              help_text="Шаблон сохраняется как черновик"
                          )
    send_count          = models.PositiveIntegerField(
                              default=0,
                              help_text="Сколько раз использован для рассылки"
                          )
    created_at          = models.DateTimeField(
                              auto_now_add=True,
                              help_text="Когда шаблон создан"
                          )
    updated_at          = models.DateTimeField(
                              auto_now=True,
                              help_text="Когда последний раз сохранялся"
                          )

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('owner', 'title')
        verbose_name = "Email шаблон"
        verbose_name_plural = "Email шаблоны"

    def __str__(self):
        return f"{self.title} ({self.owner})"
