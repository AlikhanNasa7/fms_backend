
from rest_framework import viewsets, serializers, status

from carts.models import Cart, CartItem
from products.api.serializers import ProductSerializer
from market.api.serializers import FarmSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    farm = serializers.SerializerMethodField()


    def get_product(self, obj):
        product = obj.product
        product_serializer = ProductSerializer(product)
        return product_serializer.data
    
    def get_farm(self, obj):
        farm = obj.farm
        farm_serializer = FarmSerializer(farm)
        return farm_serializer.data

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'product_id', 'quantity', 'farm_id', 'product', 'farm']
