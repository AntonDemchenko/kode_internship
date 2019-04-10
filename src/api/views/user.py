import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from base_app.models import User
from base_app.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserView(APIView):
    def get(self, request) -> Response:
        users_list = list(User.objects.all())
        return Response(dict(
            users=users_list
        ))

    def post(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
