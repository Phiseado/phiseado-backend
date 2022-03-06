from rest_framework import serializers

class CheckUrlSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200)