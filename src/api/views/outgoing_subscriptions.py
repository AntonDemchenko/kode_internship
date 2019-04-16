from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from base_app.models import Subscription
from base_app.serializers import SubscriptionSerializer


class OwnerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get('pk')


class OutgoingSubscriptionList(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated, OwnerOnly)

    def get(self, request, pk):
        subscriptions = Subscription.get_outgoing_subs(pk)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
