from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from base_app.models import Subscription
from base_app.serializers import SubscriptionSerializer


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get('user_id')


class OutgoingSubscriptionList(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner)

    @staticmethod
    def get(request, user_id):
        subscriptions = Subscription.get_outgoing(user_id)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, user_id):
        request.data['owner'] = user_id
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription = serializer.save()
            subscription.notice()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, user_id):
        target_id = request.query_params.get('target_id')
        if not target_id:
            return Response(
                {'error': 'Missing target_id query parameter.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            subscription = Subscription.get(user_id, target_id)
        except Subscription.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
