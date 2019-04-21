from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from base_app.models import Pitt
from base_app.serializers import PittSerializer


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.id == obj.user_id


class PittList(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    @staticmethod
    def get(request, user_id):
        pitts = Pitt.get_by_user_id(user_id)
        serializer = PittSerializer(pitts, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, user_id):
        request.data['user'] = user_id
        serializer = PittSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, user_id):
        pitt_id = request.query_params.get('pitt')
        if not pitt_id:
            return Response(
                {'error': 'Missing pitt query parameter.'},
                status.HTTP_400_BAD_REQUEST
            )
        try:
            pitt = Pitt.get_by_id(pitt_id)
        except Pitt.DoesNotExist:
            return Response(
                {'error': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        pitt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
