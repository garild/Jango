"""View for the user API ."""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSeriliazer,
    AuthTokenSerializer
)


class CrateUserView(generics.CreateAPIView):
    """ Create a new user in the system."""
    serializer_class = UserSeriliazer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the auth user"""

    serializer_class = UserSeriliazer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retriev and return the auth user"""
        return self.request.user
