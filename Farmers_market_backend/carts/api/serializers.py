from rest_framework.serializers import ModelSerializer, SerializerMethodField
from carts.models import Cart


class CartSerializer(ModelSerializer):
    total_price = SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        cart_items = obj.items
        total_price = 0