from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from base_app.models import Pitt
from base_app.serializers import PittSerializer


class FeedView(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)

    @staticmethod
    def get(request):
        feed = Pitt.get_feed(request.user.id)
        serializer = PittSerializer(feed, many=True)
        return Response(serializer.data)
