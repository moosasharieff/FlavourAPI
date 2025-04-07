"""
Tests for testing User APIs
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Creates users directly into the database"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITestClass(TestCase):
    def setUp(self):
        """Setting up this class to perform API tests."""
        self.client = APIClient()

    def test_create_user_success(self):
        """Tests user is created successfully."""
        # Payload for HTTP Requests
        payload = {
            "email": "test@example.com",
            "password": "testPassword123",
            "name": "Test Name",
        }

        # HTTP POST Request to create user
        res = self.client.post(path=CREATE_USER_URL, data=payload)

        # Assertions
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Asserting for email & password
        # Fetches data from db
        user = get_user_model().objects.get(email=payload["email"])
        self.assertEqual(user.email, payload["email"])

        # Asserting to check password in not present in response data
        self.assertNotIn("password", res.data)

    def test_user_email_already_exits(self):
        """Test to confirm if user email already exists in database."""
        # Payload for HTTP Requests
        payload = {
            "email": "test@example.com",
            "password": "testPassword123",
            "name": "Test Name",
        }

        # Creating user directly into db
        create_user(**payload)
        # HTTP POST Request to create user
        res = self.client.post(CREATE_USER_URL, payload)

        # Assertions
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_length_too_short_error(self):
        """Test case to raise error that password lenght is less
        than 5 characters."""
        payload = {"email": "test@example.com", "password": "test", "name": "Test Name"}

        # HTTP POST Request to create user
        res = self.client.post(path=CREATE_USER_URL, data=payload)

        # Assertions
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Checks if user was created with less password characters
        user_exists = get_user_model().objects.filter(email=payload["email"])
        self.assertFalse(user_exists)

    def test_create_token_for_valid_credentials(self):
        """Test create token successfully for valid credentials."""
        user_details = {
            "email": "test@example.com",
            "password": "testPassword@122",
            "name": "Test Name",
        }

        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
            "name": user_details["name"],
        }

        response = self.client.post(TOKEN_URL, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_token_creation_fail_for_invalid_credentials(self):
        """Test token creation is unsuccessful for invaid credentials."""
        user_details = {
            "email": "test@example.com",
            "password": "testPassword@122",
            "name": "Test Name",
        }

        create_user(**user_details)

        payload = {
            "email": "test@example.com",
            "password": "incorrectPassword@123",
            "name": "Test Name",
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_token_creation_fails_with_missiing_credentials(self):
        """Test token creation is unsuccessful with missing credentials."""
        user_details = {
            "email": "test@example.com",
            "password": "testPassword@122",
            "name": "Test Name",
        }

        create_user(**user_details)

        payload = {"email": "test@example.com", "password": "", "name": "Test Name"}

        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_retrieve_user_data_with_unauthorized_user(self):
        """Test retrieving user data with unauthorized user."""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
