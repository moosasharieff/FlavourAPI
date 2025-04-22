"""
Tests for flavour APIs.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Flavour

from ..serializers import FlavourDetailSerializer, FlavourSerializer

FLAVOUR_URL = reverse("flavour:flavour-list")


def flavour_detail_url(flavour_id):
    """Returns custom flavour URL."""
    return reverse("flavour:flavour-detail", args=[flavour_id])


def create_user(**params):
    """Create user directly in Database."""
    creds = {"email": "test@testing.com", "password": "testing"}

    creds.update(**params)
    return get_user_model().objects.create_user(
        email=creds["email"], password=creds["password"]
    )


def create_flavour(user, **params):
    """Create Flavour directly in the Database."""
    defaults = {
        "title": "Sample Title Name",
        "time_minutes": 25,
        "price": Decimal("10.5"),
        "description": "This is a sample description.",
        "link": "https://example.com",
    }
    defaults.update(**params)
    return Flavour.objects.create(user=user, **defaults)


class PublicFlavourAPITests(TestCase):
    """Test case of Flavour API for un-authorized user."""

    def setUp(self):
        """Setting up test environment."""
        self.client = APIClient()

    def test_retrieve_flavour_list_failure(self):
        """Test retrieving flavour list will fail."""
        response = self.client.get(FLAVOUR_URL)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFlavourAPITests(TestCase):
    """Test cases of Flavour API for authorized user."""

    def setUp(self):
        """Setting up testing environrment."""
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_flovours(self):
        """Test retrieve reciepes."""
        create_flavour(user=self.user)
        create_flavour(user=self.user)

        response = self.client.get(FLAVOUR_URL)
        flavour = Flavour.objects.all().order_by("-id")
        serializer = FlavourSerializer(flavour, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrive_flavour_for_user(self):
        """Test retrieving flavour for specific user."""
        other_user_creds = {
            "email": "otherTester@testing.com",
            "password": "testPassword",
        }

        other_user = create_user(**other_user_creds)

        create_flavour(self.user)
        create_flavour(other_user)

        response = self.client.get(FLAVOUR_URL)

        db_flavour_data = Flavour.objects.filter(user=self.user)
        serializer = FlavourSerializer(db_flavour_data, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_flavour_details(self):
        """Test retriving single flavour detail."""
        flavour = create_flavour(user=self.user)

        url = flavour_detail_url(flavour.id)
        response = self.client.get(url)

        serializer = FlavourDetailSerializer(flavour)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
