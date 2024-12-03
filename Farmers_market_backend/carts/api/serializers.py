
from rest_framework import viewsets, serializers, status

from carts.models import Cart, CartItem
from products.api.serializers import ProductSerializer
from market.api.serializers import FarmSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    farm = serializers.SerializerMethodField()
    description = serializers.CharField(source='product.description')
    product_image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    farm_image = serializers.SerializerMethodField()

    def get_product(self, obj):
        product = obj.product
        product_serializer = ProductSerializer(product)
        return product_serializer.data
    
    def get_farm(self, obj):
        farm = obj.farm
        farm_serializer = FarmSerializer(farm)
        return farm_serializer.data
    
    def get_farm_image(self, obj):
        farm = obj.farm
        
        return farm.image_urls[0]
    
    def get_product_image(self, obj):
        product = obj.product
        
        return product.image_urls[0]
    
    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'product_id', 'quantity', 'farm_id', 'product', 'farm_image', 'description', 'farm', 'product_image', 'total_price']
