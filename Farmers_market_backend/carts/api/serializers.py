
from rest_framework import viewsets, serializers, status

from carts.models import Cart, CartItem



class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'product_id', 'quantity', 'farm_id']
