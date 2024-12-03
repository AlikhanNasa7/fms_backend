from carts.api.serializers import CartItemSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from django.shortcuts import get_object_or_404

from carts.models import Cart, CartItem

from products.models import Product
from rest_framework import status

class CartViewset(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer


    @action(detail=False, methods=['get'], url_path='get')
    def cart_items(self, request, *args, **kwargs):
        """
        List all items in the authenticated user's cart.
        """
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
        
        try:
            cart = get_object_or_404(Cart, pk=request.user.user_id)
        except Cart.DoesNotExist:
            return Response({'detail': 'Cart not found.'}, status=400)
        
        print(cart)
        items = CartItem.objects.filter(cart_id=cart)

        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_cart_item(self, request):
        print(request.user.user_id, 123413412341234)
        cart = Cart.objects.get(pk=request.user.user_id)
        print(cart)
        # Get product and quantity from request
        print(request.data)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        print(product_id, quantity)
        if not product_id or not quantity:
            raise ValidationError("Product ID and quantity are required.")

        product = get_object_or_404(Product, pk=product_id)

        farm_id = product.farm_id
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=Product.objects.get(pk=product.product_id),
            defaults={'quantity': quantity, 'farm_id': farm_id}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data)


    @action(detail=False, methods=['put'], url_path='retract-item')
    def retract_cart_item(self, request):
        """
        Remove an item from the authenticated user's cart.
        """

        cart_item_id = request.data.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)

        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data)
    
    @action(detail=True, methods=['delete'], url_path='delete-item')
    def delete_item(self, request, pk=None):
        """
        Remove an item from the authenticated user's cart.
        """

        cart_item = get_object_or_404(CartItem, pk=pk)

        cart_item.delete()

        return Response({"message": "Deleted Successfully"}, status=status.HTTP_202_ACCEPTED)