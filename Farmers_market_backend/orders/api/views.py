from carts.api.serializers import CartItemSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from django.shortcuts import get_object_or_404

from carts.models import Cart, CartItem
from market.models import Farm
from orders.api.serializers import OrderSerializer
from orders.models import Order, OrderItem

from products.models import Product
from users.models import Buyer
from rest_framework import status


class OrderViewset(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer


    @action(detail=False, methods=['post'], url_path='add-item')
    def create_order(self, request):
        cart = get_object_or_404(Cart, pk=request.user.user_id)
        buyer = get_object_or_404(Buyer, pk=request.user.user_id)
        order = Order.objects.create(
            buyer_id=buyer,
            status = "pending",
        )

        items = CartItem.objects.filter(cart_id=cart)
        for item in items:
            print(item.product_id)
            farm_id = get_object_or_404(Farm, pk=item.farm_id_id)
            product = get_object_or_404(Product, pk=item.product_id_id)
            OrderItem.objects.create(
                order_id=order,
                product_id=product,
                quantity=item.quantity,
                farm_id=farm_id,
            )
            item.delete()


        return Response({"message": "Successfully created an order"}, status=status.HTTP_201_CREATED)