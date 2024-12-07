from rest_framework.serializers import ModelSerializer, SerializerMethodField
from orders.models import Order, OrderItem
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    buyer_name = serializers.CharField(source='buyer.user.first_name')

    class Meta:
        model = Order
        fields = [ 'status', 'buyer_id', 'created_at', 'total_price', 'buyer_name', 'order_id']

    def get_total_price(self, obj):
        return obj.get_total_price()
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.CharField(source='product.price')
    product_unit = serializers.CharField(source='product.unit_name')
    product_category = serializers.CharField(source='product.category.name')
    product_total_price = serializers.SerializerMethodField()
    product_description = serializers.CharField(source='product.description')
    farm_image = serializers.SerializerMethodField()
    farm_name = serializers.CharField(source='farm.farm_name')
    product_description = serializers.CharField(source='farm.description')
    buyer = serializers.CharField(source='order.buyer.user.email')
    created_at = serializers.DateTimeField(source='order.created_at')

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_product_image(self, obj):
        if not obj.product.image_urls or not obj.product.image_urls[0]:
            return None
        if "http" in obj.product.image_urls[0]:
            return obj.product.image_urls[0]
        return "http://127.0.0.1:8000" + obj.product.image_urls[0]
    
    def get_farm_image(self, obj):
        if not obj.farm.image_urls or not obj.farm.image_urls[0]:
            return None
        if "http" in obj.farm.image_urls[0]:
            return obj.farm.image_urls[0]
        return "http://127.0.0.1:8000" + obj.farm.image_urls[0]

    def get_product_total_price(self, obj):
        return obj.product.price * obj.quantity