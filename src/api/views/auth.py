from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class PublicKeyView(APIView):
    def get(self, request):
        return Response({
            "pubkey": settings.PUBLIC_KEY
        })
