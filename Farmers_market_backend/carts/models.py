from django.db import models
from products.models import Product
from market.models import Farm
import uuid

class Cart(models.Model):
    buyer = models.OneToOneField('users.Buyer', models.CASCADE, primary_key=True, related_name="buyers_cart")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.buyer.user.first_name}'s Cart"


class CartItem(models.Model):
    cart_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, related_name="cart_items", default=1)

    def get_total_price(self):
        return self.quantity * self.product_id.price