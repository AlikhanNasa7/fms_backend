from rest_framework.serializers import ModelSerializer, SerializerMethodField
from orders.models import Order
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [ 'status', 'buyer_id', 'created_at']
