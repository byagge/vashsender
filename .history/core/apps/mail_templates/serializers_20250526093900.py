from rest_framework import serializers
from .models import EmailTemplate

class EmailTemplateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = EmailTemplate
        fields = [
            'id',
            'owner',
            'title',
            'html_content',
            'ck_content',
            'plain_text_content',
            'is_draft',
            'send_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id','owner','send_count','created_at','updated_at']
