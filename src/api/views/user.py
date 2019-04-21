import logging

from rest_framework import generics, status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from base_app.models import User
from base_app.serializers import UserSerializer

logger = logging.getLogger(__name__)


class ReadForAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return True
        return IsAuthenticated().has_permission(request, view)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.id == obj.user_id


class UserList(generics.ListCreateAPIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (ReadForAuthenticated,)
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveDestroyAPIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSearch(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        username = request.query_params.get('username')

        if not username:
            return Response(
                {'error': 'Missing username parameter.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.get_by_username(username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
