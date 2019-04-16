from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class PublicKeyView(APIView):
    def get(self, request):
        return Response({
            'pubkey': settings.PUBLIC_KEY
        })
