import logging

from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class HeartBeatHealthCheck(APIView):
    def get(self, request):
        logger.info('Common Health: OK')
        return Response({
            'result': 'CommonOK'
        })
