"""
Serializers for the user API view.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

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

    def update(self, instance, validated_data):
        """Update and return user"""
        # .pop() will retrieve the password then remove it from the validated_data dictionary
        # if a password is not provided, it will default to None
        password = validated_data.pop('password', None)
        # calls the update() method in the base ModelSerializer class
        # must remove the password from the validated_data dictionary first, because password is not a field in the user model
        # when you call update() it will update an instance of the user model, all fields must match
        user = super().update(instance, validated_data)
        # if there is a password, set it here
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    # We do not need a ModelSerializer here just the generic one
    # because we are not validating based on model validation rules
    """Serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        # get email and password from the request body by accessing attrs
        email = attrs.get('email')
        password = attrs.get('password')
        # authenticate with the given email and password, if successful, this will return a user object
        # note that the 'request' field is required for unclear reason, just equate it to the request body
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        # if authentication fails, the user will not be set and therefore, raise the validation error with a custom message
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        # must set and return attrs['user'] so that it can be accessed in the View
        attrs['user'] = user

        return attrs
