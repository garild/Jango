"""Test user"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create && return new user."""

    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the public features of the yser API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'test1234567',
            'name': 'garib',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def user_with_emial_exists_error(self):
        """Test error return if user with email exists"""

        payload = {
            'email': 'test@example.com',
            'password': 'test1234567',
            'name': 'garib',
        }

        create_user(payload)

        res = self.client.post(create_user, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def user_with_password_to_short_error(self):
        """Test throw error on password validation"""

        payload = {
            'email': 'test@example.com',
            'password': '1234',
            'name': 'garib',
        }

        res = self.client.post(create_user, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(payload['email']).exists()
        self.assertFalse(user_exists)
