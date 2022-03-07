from rest_framework import serializers

class CheckUrlSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)