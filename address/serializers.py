"""
Serializers for Address APIs.
"""
from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address."""

    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'country', 'latitude', 'longitude']
        read_only_fields = ['id']


class AddressDetailSerializer(AddressSerializer):
    """Serializer for address detail view."""

    class Meta(AddressSerializer.Meta):
        fields = AddressSerializer.Meta.fields
