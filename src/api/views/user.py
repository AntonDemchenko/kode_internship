import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from base_app.models import User

logger = logging.getLogger(__name__)


class UserView(APIView):
    def get(self, request) -> Response:
        users_list: list = list(User.objects.all())
        return Response(dict(
            users=users_list
        ))
