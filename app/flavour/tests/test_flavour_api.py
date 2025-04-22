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

    def test_create_flavour_api(self):
        """Test create Flavour from API."""
        payload = {
            "title": "Sample Flavour",
            "time_minutes": 35,
            "price": Decimal("3.29"),
        }

        response = self.client.post(FLAVOUR_URL, payload)

        flavour_data = Flavour.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(flavour_data.user, self.user)

        for key, value in payload.items():
            self.assertEqual(getattr(flavour_data, key), value)

    def test_partial_update(self):
        """Test updating the fields of a Flavour partially."""
        flavour = create_flavour(user=self.user)

        payload = {
            "title": "Updated tile of Flavour",
            "time_minutes": 30,
        }

        url = flavour_detail_url(flavour.id)
        response = self.client.patch(url, payload)

        flavour.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flavour.title, payload["title"])
        self.assertEqual(flavour.time_minutes, payload["time_minutes"])
        self.assertEqual(flavour.user, self.user)

    def test_full_update(self):
        """Test updating all the fields of an existing flavour."""
        flavour = create_flavour(user=self.user)

        payload = {
            "title": "New Sample Title Name",
            "time_minutes": 30,
            "price": Decimal("12.5"),
            "description": "This is a new sample description.",
            "link": "https://new_example.com",
        }

        url = flavour_detail_url(flavour.id)
        response = self.client.put(url, payload)

        flavour.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flavour.user, self.user)
        for key, value in payload.items():
            self.assertEqual(getattr(flavour, key), value)

    def test_assigning_new_flavour_user_fails(self):
        """Test assigning new owner for an existing flavour fails."""
        creds = {
            "email": "otherTester@gmail.com",
            "password": "OtherPassword@123",
            "name": "OtherUser",
        }

        other_user = create_user(**creds)
        other_client = APIClient()
        other_client.force_authenticate(other_user)

        flavour = create_flavour(user=self.user)

        payload = {"user": other_user.id}

        url = flavour_detail_url(flavour.id)
        response = other_client.patch(url, payload)

        flavour.refresh_from_db()

        self.assertEqual(flavour.user, self.user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_flavour(self):
        """Test successfully deleting a flavour."""
        flavour = create_flavour(user=self.user)

        url = flavour_detail_url(flavour.id)
        response = self.client.delete(url)

        is_flavour_present = Flavour.objects.filter(id=flavour.id).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(is_flavour_present)

    def test_delete_other_user_flavour_failure(self):
        """Test deleting other user's recipe and failure to do so."""
        flavour = create_flavour(user=self.user)

        creds = {
            "email": "otherTester@gmail.com",
            "password": "TestPassword",
        }
        other_user = create_user(**creds)
        other_client = APIClient()
        other_client.force_authenticate(other_user)

        url = flavour_detail_url(flavour.id)
        response = other_client.delete(url)

        is_flavour_present = Flavour.objects.filter(id=flavour.id).exists()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(is_flavour_present)
