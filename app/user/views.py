"""
Views for the user API
"""

# rest_framework handles a lot of logics for creating objects in the database for us
# by providing a bunch of base classes that we can configure for our views that will handle requests
# in a default standardized way, at the same time we have the ability to modify it as we need
from rest_framework import generics, authentication, permissions

# DRF provides a View for getting the auth token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    # CreateAPIView handles a HTTP post request designed for creating objects
    """Create a new user in the system"""
    # set the serializer for this view so Django knows what serializer to use
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    # optional, to add nice UI style classes for this View
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user
