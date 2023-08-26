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

    def test_new_user_email_normalized(self):
        """ Test email is normalized for new users """

        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
