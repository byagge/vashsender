from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import EmailTemplate
from .serializers import EmailTemplateSerializer
from rest_framework.decorators import action
from apps.

class EmailTemplateViewSet(viewsets.ModelViewSet):
    serializer_class    = EmailTemplateSerializer
    permission_classes  = [IsAuthenticated]

    def get_queryset(self):
        return EmailTemplate.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='increment-send-count')
    def increment_send_count(self, request, pk=None):
        template = self.get_object()
        template.send_count = models.F('send_count') + 1
        template.save(update_fields=['send_count'])
        template.refresh_from_db()
        return Response({'send_count': template.send_count})
