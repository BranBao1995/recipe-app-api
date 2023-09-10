"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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

        # create a user in the test database
        create_user(**payload)

        # try to create another user with the same user info by making a client POST request, store response data in a variable
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

    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""

        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }

        # registers the user
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        # user login to get the token by posting to TOKEN_URL
        res = self.client.post(TOKEN_URL, payload)
        # check to see if the token is returned as part of the response data
        self.assertIn('token', res.data)
        # check status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials are invalid"""

        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""

        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users"""

        res = self.client.get(ME_URL)
        # unauthenticated because this test class is a public class
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        res = self.client.get(ME_URL)

        # status code should be 200 because the user is authenticated
        # check if returned user info is correct
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user"""

        payload = {'name': 'Updated name', 'password': 'newpassword123'}
        # update user credentials with PATCH method
        res = self.client.patch(ME_URL, payload)
        # refresh the database to reflect the change
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
