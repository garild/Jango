"""View for the user API ."""

from rest_framework import generics

from user.serializers import UserSeriliazer


class CrateUserView(generics.CreateAPIView):
    """ Create a new user in the system."""
    serializer_class = UserSeriliazer
