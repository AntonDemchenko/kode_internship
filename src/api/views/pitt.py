from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base_app.serializers import PittSerializer


class PittList(APIView):

    @staticmethod
    def post(request, user_id):
        request['user'] = user_id
        serializer = PittSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
