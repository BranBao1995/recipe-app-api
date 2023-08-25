"""
Tests for models.
"""

from django.test import TestCase
# helper function to help get the default user model while not directly importing the actual defined user model in models.py
# it is the best practice to use get_user_model because even if you modify you custom user model later, this will still
# automatically retrieve the default user model
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):

        email = 'test@example.com'
        password = 'testpass123'

        # retrieve the default user model with get_user_model, call user manager and simulate user creation
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        # check if the correct email has been assigned to the user
        self.assertEqual(user.email, email)
        # check if the correct password has been assigned to the user
        self.assertTrue(user.check_password(password))
