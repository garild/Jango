"""
Test for models
"""


from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
    """Test models."""

    def test_create_user_with_email_successfull(self):
        """Test create a user with an email is successfull."""
        email = 'tests@example.pl'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email, password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if new user email is normalized"""

        sameple_emails = [
            ['test@EXSAMPLE.com', 'test@exsample.com'],
            ['TEST2@EXAmple.pl', 'TEST2@example.pl'],
            ['TEST1@GMAIL.COM', 'TEST1@gmail.com']
        ]
        for email, expected in sameple_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_withour_email_raises_error(self):
        """Test that creating user w/o emial raises expection"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'password123')

    def test_create_superuser(self):
        """Test creating a supersuer."""
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'test123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
