from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from . import serializers
from django.views.decorators.csrf import csrf_exempt
from .services import phishing_system

class check_url_blacklist(generics.CreateAPIView):
    serializer_class = serializers.CheckUrlSerializer

    @csrf_exempt
    def post(self, request):
        body = request.data
        message = body['message']
        phishing = phishing_system.check_message(message)
        return Response(
            data={"result": True if phishing else False}, 
            status=HTTP_200_OK
        )
