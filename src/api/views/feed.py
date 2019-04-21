from django.conf import settings
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from base_app.models import Pitt
from base_app.serializers import PittSerializer


class FeedView(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)

    @staticmethod
    def get(request):
        all_feed = Pitt.get_feed(request.user.id)
        paginator = Paginator(all_feed, settings.ITEMS_PER_PAGE)
        page = request.query_params.get('page')
        feed = paginator.get_page(page)
        serializer = PittSerializer(feed, many=True)
        return Response(serializer.data)
