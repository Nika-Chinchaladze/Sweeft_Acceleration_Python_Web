from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    client_name = serializers.CharField(max_length=200)
    is_premium = serializers.CharField(max_length=10)
    original_link = serializers.CharField(max_length=1000)
    