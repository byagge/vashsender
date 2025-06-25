# emails/models.py
import uuid
from django.db import models
from django.conf import settings

class Domain(models.Model):
    owner               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    domain_name         = models.CharField(max_length=255, unique=True)
    is_verified         = models.BooleanField(default=False)
    spf_verified        = models.BooleanField(default=False)
    dkim_verified       = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=32, unique=True, editable=False)
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain_name
