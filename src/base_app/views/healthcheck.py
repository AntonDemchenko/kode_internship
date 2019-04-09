import logging

from rest_framework.views import APIView
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class HeartBeatHealthCheck(APIView):
    def get(self, request):
        logger.info('Common Health: OK')
        return Response({
            "result": "CommonOK"
        })
