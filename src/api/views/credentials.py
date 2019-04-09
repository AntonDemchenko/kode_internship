import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from base_app.utils.redis import save_pwd, get_pwd

logger = logging.getLogger(__name__)


class CredentialsView(APIView):
    def post(self, request) -> Response:
        data = request.data
        login = data.get('login', None)
        pwd = data.get('password', None)

        if not login or not pwd:
            return Response(
                dict(
                    code='validation_error',
                    message='Check fields!'
                ),
                status=400
            )

        result = save_pwd(login, pwd)

        return Response(dict(
            result=result
        ))

    def get(self, request) -> Response:
        data = request.data
        login = data.get('login', None)

        if not login:
            return Response(
                dict(
                    code='validation_error',
                    message='Check fields!'
                ),
                status=400
            )

        pwd = get_pwd(login)

        return Response(dict(
            password=pwd
        ))
