# core/apps/mail_templates/serializers.py
from rest_framework import serializers
from .models import EmailTemplate

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = [
            'id',
            'title',
            'html_content',
            'plain_text_content',
            'ck_content',
            'is_draft',
            'send_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['send_count', 'created_at', 'updated_at']
