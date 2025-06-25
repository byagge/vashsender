# core/apps/emails/serializers.py

from rest_framework import serializers
from .models import Domain, SenderEmail

class DomainSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Domain
        fields = [
            'id', 'owner', 'domain_name',
            'is_verified', 'spf_verified', 'dkim_verified',
            'verification_token', 'created_at',
        ]
        read_only_fields = ['id', 'is_verified', 'spf_verified', 'dkim_verified', 'verification_token', 'created_at']

# core/apps/emails/serializers.py

from rest_framework import serializers
from .models import SenderEmail
class SenderEmailSerializer(serializers.ModelSerializer):
    domain_name = serializers.SerializerMethodField()

    class Meta:
        model = SenderEmail
        fields = [
            'id',
            'email',
            'domain',        # FK ID
            'domain_name',   # human-readable
            'is_verified',
            'verification_token',
            'created_at',
            'verified_at',   # если в модели есть поле verified_at
            # убрали updated_at
        ]
        read_only_fields = fields

    def get_domain_name(self, obj):
        return obj.domain.domain_name