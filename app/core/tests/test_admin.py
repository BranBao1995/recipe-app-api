"""
Test for the Django admin modification
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django Admin"""

    # setup before testing
    def setUp(self):
        """Create user and client."""

        # Client() acts as a dummy browser which allows you to test your views
        # Read more https://docs.djangoproject.com/en/4.2/topics/testing/tools/
        self.client = Client()

        # create a superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )

        # force login with the superuser's credentials so that any actions after will be authenticated with the admin user
        self.client.force_login(self.admin_user)

        # create a user
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on page."""

        # use reverse() to get the url of changelist which includes a list of users
        url = reverse('admin:core_user_changelist')

        # res contains the response of the url (changelist)
        res = self.client.get(url)

        # check if the response contains the user
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test if the create user page works."""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
