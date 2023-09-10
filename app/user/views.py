"""
Views for the user API
"""

# rest_framework handles a lot of logics for creating objects in the database for us
# by providing a bunch of base classes that we can configure for our views that will handle requests
# in a default standardized way, at the same time we have the ability to modify it as we need
from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    # CreateAPIView handles a HTTP post request designed for creating objects
    """Create a new user in the system"""

    # set the serializer for this view so Django knows what serializer to use
    serializer_class = UserSerializer
