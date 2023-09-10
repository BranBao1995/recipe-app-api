"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        # APIClient mocks user authentication such as user registration & login
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        # new user credentials
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # post request to register the user, store response data in a variable
        res = self.client.post(CREATE_USER_URL, payload)

        # check response status code to see if the user is created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # retrieve newly created user and store it in a variable
        user = get_user_model().objects.get(email=payload['email'])

        # check if the user's password is the same as the one given in the payload
        self.assertTrue(user.check_password(payload['password']))

        # check to make sure the user password is not included in the response data
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # create a user in the database
        create_user(**payload)

        # try to create another user with the same user info by mocking a client POST request, store response data in a variable
        res = self.client.post(CREATE_USER_URL, payload)

        # response status code should be 400 because the user already exists in the database
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""

        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        # should return a bad request because password is too short
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # to be safe, we also want to check the user actually was not created and stored in the database
        # user_exists stores a boolean value
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
