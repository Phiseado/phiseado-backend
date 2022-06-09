from rest_framework import serializers

class CheckUrlSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)

class DomainSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    frequency = serializers.IntegerField()