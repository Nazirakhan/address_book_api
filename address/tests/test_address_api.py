"""
Test for address APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from address.models import Address

from address.serializers import (
    AddressSerializer,
    AddressDetailSerializer,
)

ADDRESS_URL = reverse('address:address-list')


def detail_url(address_id):
    """Create and return a address detail URL."""
    return reverse('address:address-detail', args=[address_id])


def create_address(user, **params):
    """Create and return a sample address."""
    defaults = {
        'street': 'Sample address',
        'city': 'Test City',
        'state': 'Test state',
        'country': 'Test Country',
        'latitude' : Decimal('10.876'),
        'longitude' : Decimal('57.98'),
    }
    defaults.update(params)

    addr = Address.objects.create(user=user, **defaults)
    return addr


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)



class PublicAddressApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(ADDRESS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAddressApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_address(self):
        """Test retrieving a list of address."""
        create_address(user=self.user)
        create_address(user=self.user)

        res = self.client.get(ADDRESS_URL)

        addrs = Address.objects.all().order_by('-id')
        serializer = AddressSerializer(addrs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_address_list_limited_to_user(self):
        """test list of address is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_address(user=other_user)
        create_address(user=self.user)

        res = self.client.get(ADDRESS_URL)

        addrs = Address.objects.filter(user=self.user)
        serializer = AddressSerializer(addrs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_address_detail(self):
        """test get_address_detail."""
        addrs = create_address(user=self.user)

        url = detail_url(addrs.id)
        res = self.client.get(url)

        serializer = AddressDetailSerializer(addrs)
        self.assertEqual(res.data, serializer.data)

    def test_create_address(self):
        """Test creating a address."""
        payload = {
            'street': 'Sample street',
            'city': 'Sample city',
            'country': 'Sample country',
            'state': 'sample state',
            'longitude': Decimal('24.8765'),
            'latitude': Decimal('56.7565'),
        }
        res = self.client.post(ADDRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        addrs = Address.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(addrs, k), v)
        self.assertEqual(addrs.user, self.user)

    def test_partial_update(self):
        """Test partial update of an address."""
        original_city = 'example city'
        addr = create_address(
            user=self.user,
            street='Sample street',
            city=original_city,
        )

        payload = {'street': 'New street'}
        url = detail_url(addr.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        addr.refresh_from_db()
        self.assertEqual(addr.street, payload['street'])
        self.assertEqual(addr.city, original_city)
        self.assertEqual(addr.user, self.user)

    def test_full_update(self):
        """Test full update of address."""
        addr = create_address(
            user=self.user,
            street='Sample Street',
            city='sample city',
            state='Sample state',
        )

        payload = {
            'street': 'New Street',
            'city': 'New City',
            'state': 'New State',
            'country': 'New Country',
            'latitude': Decimal('25.47620'),
            'longitude': Decimal('74.5780'),

        }
        url = detail_url(addr.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        addr.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(addr, k), v)
        self.assertEqual(addr.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the address user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        addr = create_address(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(addr.id)
        self.client.patch(url, payload)

        addr.refresh_from_db()
        self.assertEqual(addr.user, self.user)

    def test_delete_address(self):
        """Test deleting a address successful."""
        addr = create_address(user=self.user)

        url = detail_url(addr.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Address.objects.filter(id=addr.id).exists())

    def test_delete_other_users_address_error(self):
        """Test trying to delete another users address gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        addr = create_address(user=new_user)

        url = detail_url(addr.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Address.objects.filter(id=addr.id).exists())