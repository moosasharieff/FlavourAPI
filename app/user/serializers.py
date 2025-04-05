"""
Serializer for the USER API View.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    class Meta:
        """Defining the params to include in DB and
        validation conditions to be applied for user provided data."""
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'min_length' : 6,
            }
        }

        def create(self, validated_data):
            """Create and return user object with encrypted data."""
            return get_user_model().objects.create_user(**validated_data)