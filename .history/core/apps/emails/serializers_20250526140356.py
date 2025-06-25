# core/apps/emails/serializers.py

from rest_framework import serializers
from .models import Domain, SenderEmail

class DomainSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Domain
        fields = [
            'id', 'owner',
            'domain_name',
            'is_verified', 'spf_verified', 'dkim_verified',
            'verification_token',
            'created_at',
        ]
        read_only_fields = ['id','is_verified','spf_verified','dkim_verified','created_at','verification_token']


class SenderEmailSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SenderEmail
        fields = [
            'id', 'owner',
            'email',
            'domain',
            'verified',        # добавьте булево поле verified и verification_token в модель, если нужно
            'verification_token',
            'created_at',
        ]
        read_only_fields = ['id','verified','verification_token','created_at']
