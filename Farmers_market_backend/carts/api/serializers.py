from rest_framework.serializers import ModelSerializer, SerializerMethodField
from carts.models import Cart

from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError

from carts.models import Cart, CartItem
from products.models import Product
from market.models import Farm
from users.models import Buyer


# class CartSerializer(ModelSerializer):
#     total_price = SerializerMethodField()
#
#     class Meta:
#         model = Cart
#         fields = '__all__'
#
#     def get_total_price(self, obj):
#         cart_items = obj.items
#         total_price = 0


class CartItemSerializer(serializers.ModelSerializer):
    # product_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'product_id', 'quantity', 'farm_id']

    # def validate(self, data):
    #     # Ensure the product exists
    #     product = data.get('product_id')
    #     if not Product.objects.filter(product_id=product).exists():
    #         raise ValidationError("Product does not exist.")
    #
    #     # Ensure quantity is valid
    #     if data.get('quantity') <= 0:
    #         raise ValidationError("Quantity must be a positive integer.")
    #
    #     # Validate if the cart belongs to the authenticated user
    #     if not self.context['request'].user.is_authenticated:
    #         raise ValidationError("User must be authenticated to add items.")
    #
    #     return data

    # def get_product_name(self, obj):
    #     # Fetching the product name from the related product_id
    #     return obj.product_id.name  # Assuming `name` is the field in the Product model