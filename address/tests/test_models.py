"""
Test for user models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from address import models

# Create your tests here.

class ModelTests(TestCase):
    """Test Models."""

    def test_create_addressbook(self):
        """Test creating a addressbook."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        addressbook = models.Address.objects.create(
            user=user,
            street='Test street',
            city = 'Test City',
            state = 'Test State',
            country = 'Test Country',
            longitude = Decimal('10.687'),
            latitude = Decimal('59.8876'),
        )

        self.assertEqual(str(addressbook), addressbook.street)