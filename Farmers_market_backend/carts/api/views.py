from rest_framework import viewsets
from carts.models import Cart
from carts.api.serializers import CartSerializer

class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer