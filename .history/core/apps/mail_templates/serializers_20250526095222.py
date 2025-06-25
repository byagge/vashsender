# mail_templates/serializers.py

from rest_framework import serializers
from .models import EmailTemplate

class EmailTemplateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EmailTemplate
        fields = [
            'id', 'owner', 'title',
            'html_content', 'ck_content',      # <-- добавили
            'plain_text_content',
            'is_draft', 'send_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'send_count', 'created_at', 'updated_at']
