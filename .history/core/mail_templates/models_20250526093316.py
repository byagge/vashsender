from django.conf import settings
from django.db import models
from django.utils import timezone

class TemplateCategory(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class EmailTemplate(models.Model):
    owner        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category     = models.ForeignKey(TemplateCategory, null=True, blank=True, on_delete=models.SET_NULL)
    name         = models.CharField(max_length=150)
    subject      = models.CharField(max_length=200)
    body_html    = models.TextField(help_text="HTML-шаблон письма")
    body_text    = models.TextField(blank=True, help_text="Альтернативный текстовый вариант")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    is_active    = models.BooleanField(default=True)

    class Meta:
        unique_together = ('owner','name')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.owner})"
