""" Serilizers for the user API view - json format"""


from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSeriliazer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validate_data):
        """Craete and return user with encrypted password"""

        return get_user_model().objects.create_user(**validate_data)
