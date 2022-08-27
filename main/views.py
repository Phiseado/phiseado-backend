from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from . import serializers
from django.views.decorators.csrf import csrf_exempt
from .services import phishing_system
import re
from .models import Message, Domain, Country
import pytz
from urllib.parse import urlparse
from django.db.models import Count
from datetime import datetime
from datetime import timedelta

class check_url_blacklist(generics.CreateAPIView):
    serializer_class = serializers.CheckUrlSerializer

    @csrf_exempt
    def post(self, request):
        body = request.data
        if 'message' in body:
            message = body['message']
            phishing = phishing_system.check_message(message)
            if phishing is None:
                return Response( 
                    status=HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    data=phishing,
                    status=HTTP_200_OK
                )
        else:
            return Response(
                status=HTTP_400_BAD_REQUEST
            )

class obtain_phishing_message(generics.CreateAPIView):
    serializer_class = serializers.ReportMessageSerializer

    @csrf_exempt
    def post(self, request):
        body = request.data
        if 'message' in body and 'isoCode' in body and 'isPhishing' in body:
            message = body['message']
            url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            if len(url) is 0:
                return Response(
                    status=HTTP_400_BAD_REQUEST
                )
            iso_code = body['isoCode'].lower()
            try:
                country_name = pytz.country_names[iso_code]
            except KeyError:
                return Response(
                    status=HTTP_400_BAD_REQUEST
                )
            country = Country.objects.get_or_create(name=country_name, country_iso_code=iso_code)

            domain_name = urlparse(url[0]).netloc
            domain = Domain.objects.get_or_create(name=domain_name)

            if body['isPhishing']:
                domain[0].frequency += 1
                domain[0].save()

            Message.objects.create(
                url=url[0],
                considered_phishing=body['isPhishing'],
                country=country[0],
                domain=domain[0]
            )

            return Response(
                    data={"result": True},
                    status=HTTP_200_OK
                )

        else:
            return Response(
                status=HTTP_400_BAD_REQUEST
            )

class domain_list(generics.ListAPIView):
    serializer_class = serializers.DomainSerializer

    def get_queryset(self):
        return Domain.objects.all().filter(frequency__gt=0).order_by('-frequency')


class pie_chart(generics.ListAPIView):
    serializer_class = serializers.PieChartSerializer

    def get(self, request):
        phishing_messages = Message.objects.filter(considered_phishing=True).count()
        non_phishing_messages = Message.objects.filter(considered_phishing=False).count()
        return Response(
            data={"phishing": phishing_messages, "non_phishing": non_phishing_messages},
            status=HTTP_200_OK
        )

class bar_chart(generics.CreateAPIView):
    serializer_class = serializers.BarChartSerializer

    @csrf_exempt
    def post(self, request):
        if 'filter' in request.data:
            if request.data['filter'] == "Este mes":
                chart = Message.objects.filter(registered_date__gt=datetime.now() - timedelta(days=30)).filter(considered_phishing=True).values('country__name').annotate(total=Count('country__name')).order_by('-total')[:3]
            elif request.data['filter'] == "Hoy":
                chart = Message.objects.filter(registered_date__gt=datetime.now() - timedelta(days=1)).filter(considered_phishing=True).values('country__name').annotate(total=Count('country__name')).order_by('-total')[:3]
            elif request.data['filter'] == "Esta semana":
                chart = Message.objects.filter(registered_date__gt=datetime.now() - timedelta(days=7)).filter(considered_phishing=True).values('country__name').annotate(total=Count('country__name')).order_by('-total')[:3]
            else:
                return Response(
                    status=HTTP_400_BAD_REQUEST)
            return Response(
                data={"chart": chart},
                status=HTTP_200_OK
            )
        else:
            return Response(
                status=HTTP_400_BAD_REQUEST)
