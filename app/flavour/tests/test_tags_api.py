"""
Tests for tag APIs
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from ..serializers import TagSerializer

TAG_URL = reverse("recipe:tag-list")


def create_user(**new_creds):
    """Create user directly in database."""
    creds = {"email": "test@testing.com", "password": "testPassword"}
    creds.update(new_creds)
    return get_user_model().objects.create_user(creds)


def create_tag(user, name):
    return Tag.objects.create(user, name)


class PublicTagAPITests(TestCase):
    """User un-authorized test class."""

    def setUp(self):
        """Setting up Test Environment."""
        self.client = APIClient()

    def test_retireve_tag_fail(self):
        """Test retrieving tags fail without authentication."""
        response = self.client.get(TAG_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
