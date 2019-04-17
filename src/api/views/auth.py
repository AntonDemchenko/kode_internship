from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class PublicKeyView(APIView):

    @staticmethod
    def get(request):
        return Response({
            'pubkey': settings.PUBLIC_KEY
        })
