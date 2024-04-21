"""
Views for the Address APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Address
from . import serializers

# Create your views here.

class AddressViewSet(viewsets.ModelViewSet):
    """ view for manage Address APIs."""
    serializer_class = serializers.AddressDetailSerializer
    queryset = Address.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve address for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.AddressSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new address."""
        serializer.save(user=self.request.user)