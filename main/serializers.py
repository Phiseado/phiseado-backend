from rest_framework import serializers

class CheckUrlSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
class DomainSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    frequency = serializers.IntegerField()

class PieChartSerializer(serializers.Serializer):
    phishing = serializers.IntegerField()
    non_phishing = serializers.IntegerField()

class BarChartSerializer(serializers.Serializer):
    country__name = serializers.CharField(max_length=200)
    total = serializers.IntegerField()