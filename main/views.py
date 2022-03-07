from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
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
        url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)[0]
        print(url)
        result = googleapi.check_url(url)
        return Response(
            data={"result": ("Este sitio web parece ser seguro", "Este sitio web no es seguro")[result]}, 
            status=HTTP_200_OK
        )

