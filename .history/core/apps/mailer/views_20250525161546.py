from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import ContactList, Contact
from .serializers import ContactListSerializer, ContactSerializer

from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .utils import parse_emails

class ContactListViewSet(viewsets.ModelViewSet):
    """
    CRUD для ContactList и вложенные операции с Contact через @action.
    """
    serializer_class = ContactListSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser] + ModelViewSet.parser_classes

    def get_queryset(self):
        return ContactList.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get','post'], url_path='contacts')
    def contacts(self, request, pk=None):
        """
        GET  /contactlists/{pk}/contacts/  — список контактов
        POST /contactlists/{pk}/contacts/  — добавить контакт { email, status }
        """
        contact_list = self.get_object()

        if request.method == 'GET':
            qs = contact_list.contacts.all()
            ser = ContactSerializer(qs, many=True)
            return Response(ser.data)

        # POST
        ser = ContactSerializer(data=request.data)
        if ser.is_valid():
            ser.save(contact_list=contact_list)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='contacts/(?P<cid>[^/.]+)')
    def delete_contact(self, request, pk=None, cid=None):
        """
        DELETE /contactlists/{pk}/contacts/{cid}/
        """
        contact_list = self.get_object()
        contact = get_object_or_404(Contact, pk=cid, contact_list=contact_list)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='import')
    def import_contacts(self, request, pk=None):
        contact_list = self.get_object()
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            emails = parse_emails(file_obj, file_obj.name)
        except Exception as e:
            return Response({'detail': f'Error parsing file: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        added = 0
        for email in emails:
            obj, created = Contact.objects.get_or_create(
                contact_list=contact_list,
                email=email,
                defaults={'status': Contact.VALID}
            )
            if created:
                added += 1

        return Response({'imported': added}, status=status.HTTP_201_CREATED)
    
# mailer/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ListSpaView(LoginRequiredMixin, TemplateView):
    # если ваш шаблон лежит в templates/list.html
    template_name = 'list.html'
