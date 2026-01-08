from rest_framework import serializers
from .models import Client, Deal

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'email', 'created_at']

class DealSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = Deal
        fields = ['id', 'title', 'amount', 'status', 'client', 'client_name', 'created_at']