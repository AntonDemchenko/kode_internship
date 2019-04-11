import logging

from rest_framework import generics

from base_app.models import User
from base_app.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
