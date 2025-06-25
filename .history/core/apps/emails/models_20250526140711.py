# core/apps/emails/models.py

from django.conf import settings
from django.db import models
import uuid

class Domain(models.Model):
    owner               = models.ForeignKey(
                              settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='domains'
                          )
    domain_name         = models.CharField(max_length=255)
    is_verified         = models.BooleanField(default=False)
    spf_verified        = models.BooleanField(default=False)
    dkim_verified       = models.BooleanField(default=False)
    verification_token  = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner','domain_name')
        ordering = ['-created_at']

    def __str__(self):
        return self.domain_name
