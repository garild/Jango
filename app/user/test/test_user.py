"""Test user"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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

    def test_create_token_for_user(self):
        """Test generate token for the valid creds"""

        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-123456'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if credentials invalid."""

        create_user(email='test@o2.pl', password='badpassword')

        payload = {'email': 'password', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertIsNot('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting blank password return an error"""

        payload = {'email': 'test@o2.pl', 'password': ''}

        res = self.client.post(TOKEN_URL, payload)

        self.assertIsNot('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorize(self):
        """Test auth is required for users"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API request that is required authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            name='Test User name',
            password='password_12345678'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_secussess(self):
        """Test retrieving profile for log user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Post is not allowed for the Me endpoint"""

        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_updaetd_user_profile(self):
        """Tet update user profile or authentificate user"""

        payload = {'name': 'updated name', 'password': 'it-new-password'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
