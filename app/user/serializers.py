"""
Serializers for the user API view.
"""

from django.contrib.auth import get_user_model

# Serializer is a way to convert to and from Python object
# It takes a JSON input and validate the input as per our validation rule, then convert it to either a Python object
# or a model in our database
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        # tell the serializer which model is being represented
        model = get_user_model()
        # a list of fields we want available in the serializer
        fields = ['email', 'password', 'name']
        # allows us to provide a dictionary of additional meta data to the fields
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        """Overwrites the serializer's own create method so that the password is encrypted"""
        # create the user with already validated data
        return get_user_model().objects.create_user(**validated_data)
