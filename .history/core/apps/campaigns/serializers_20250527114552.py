# core/apps/campaigns/serializers.py

from rest_framework import serializers
from .models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Campaign
        fields = [
            'id', 'owner', 'name', 'template', 'sender_email',
            'subject', 'sender_name', 'reply_to',
            'contact_lists', 'scheduled_at',
            'status', 'created_at', 'sent_at',
        ]
        read_only_fields = ['id', 'owner', 'status', 'created_at', 'sent_at']
