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

from ..serializers import FlavourSerializer

FLAVOUR_URL = "flavour:flavour-list"


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

