# emails/serializers.py
from rest_framework import serializers
from .models import Domain

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id','domain_name','is_verified','spf_verified','dkim_verified','verification_token','created_at']
        read_only_fields = ['id','is_verified','spf_verified','dkim_verified','verification_token','created_at']
