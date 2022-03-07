from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from . import serializers
from django.views.decorators.csrf import csrf_exempt
from .services import googleapi
import re

# Create your views here.
class check_url_blacklist(generics.CreateAPIView):
    serializer_class = serializers.CheckUrlSerializer

    @csrf_exempt
    def post(self, request):
        body = request.data
        message = body['message']
        url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        if len(url) > 0:
            url = url[0]
            result = googleapi.check_url(url)
            return Response(
                data={"result": (False, True)[result]}, 
                status=HTTP_200_OK
            )
        else:
            return Response( 
                status=HTTP_400_BAD_REQUEST
            )
