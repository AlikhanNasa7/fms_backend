from carts.api.serializers import CartItemSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from django.shortcuts import get_object_or_404

from carts.models import Cart, CartItem
from market.models import Farm
from orders.api.serializers import OrderSerializer, OrderItemSerializer
from orders.models import Order, OrderItem, Delivery

from products.models import Product
from users.models import Buyer, CustomUser, Farmer
from rest_framework import status


class OrderViewset(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer


    
    def retrieve(self, request, pk=None):
        user = request.user
        print(user)
        buyer = Buyer.objects.get(user=user)

        order = Order.objects.get(pk=pk,buyer=buyer)

        order_serializer = OrderSerializer(order)
        # delivery_id = str(order.pk) +'_'+ str(order.items[].farm.pk)
        # print(delivery_id)
        # delivery = Delivery.objects.get(pk=delivery_id)
        # print(delivery)
        user_info = {
            "name": f"{buyer.user.first_name} {buyer.user.last_name}",
            "email": buyer.user.email
        }

        order_items = OrderItem.objects.filter(order__buyer=buyer, order=order)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        data = {
            "order": order_serializer.data,
            "user": user_info,
            "order_items": order_items_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='farm-orderitems')
    def get_farm_orderitems(self, request):
        user = request.user
        
        order_items = OrderItem.objects.filter(farm__farmer_id=user.user_id)

        order_items_serializer = OrderItemSerializer(order_items, many=True)

        return Response(order_items_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='get')
    def get(self, request):
        user = request.user
        print(user)
        if user.role=='Buyer':
            buyer = Buyer.objects.get(user=user)

            orders = Order.objects.filter(buyer=buyer).order_by('-created_at')

            orders_serializer = OrderSerializer(orders, many=True)

            return Response(orders_serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request):
        cart = get_object_or_404(Cart, pk=request.user.user_id)
        buyer = get_object_or_404(Buyer, pk=request.user.user_id)
        order = Order.objects.create(
            buyer=buyer,
            status = "pending",
        )

        items = CartItem.objects.filter(cart_id=cart)
        for item in items:
            print(item.product_id)
            farm_id = get_object_or_404(Farm, pk=item.farm_id)
            product = get_object_or_404(Product, pk=item.product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                farm=farm_id,
            )
            # Decreasing in product quantity from farmer 
            product.quantity-=item.quantity
            product.save()
            item.delete()


        return Response({"message": "Successfully created an order"}, status=status.HTTP_201_CREATED)