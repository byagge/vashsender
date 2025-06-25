# apps/emails/serializers.py

import re
from rest_framework import serializers
from .models import Domain

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = [
            'id',
            'domain_name',
            'is_verified',
            'spf_verified',
            'dkim_verified',
            'verification_token',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'is_verified',
            'spf_verified',
            'dkim_verified',
            'verification_token',
            'created_at',
        ]

    def validate_domain_name(self, value):
        """
        Должен быть в формате name.tld
        не более одного уровня (например, example.com или foo.io)
        """
        # простой regex: буквы/цифры/дефис, точка, минимум 2 буквы в TLD
        if not re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError(
                "Неверный формат домена. Должно быть вида example.com"
            )
        return value.lower()
