from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
)
from . import serializers
from django.views.decorators.csrf import csrf_exempt
from .services import googleapi

# Create your views here.
class check_url_blacklist(generics.CreateAPIView):
    serializer_class = serializers.CheckUrlSerializer

    @csrf_exempt
    def post(self, request):
        body = request.data
        url = body['url']
        result = googleapi.check_url(url)
        return Response(
            data={"result": ("Este sitio web parece ser seguro", "Este sitio web no es seguro")[result]}, 
            status=HTTP_200_OK
        )

