from django.db import models
from users.models import Buyer, Farmer
from products.models import Product
from market.models import Farm
import uuid

class Order(models.Model):
    order_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        max_length=36
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    buyer_id = models.ForeignKey(Buyer, models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])



class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=20, choices=[
        ('kg', 'kg'),
        ('pcs', 'pcs'),
        ('litres', 'litres')
    ])
    quantity = models.PositiveIntegerField()
    farm_id = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, related_name="order_items", default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price


class Delivery(models.Model):
    delivery_id = models.CharField(max_length=75, primary_key=True)
    delivery_method = models.CharField(max_length=20, choices=[
        ('pickup', 'pickup'),
        ('courier', 'courier')
    ], default='courier')
    STATUS = (
        ('paid', 'paid'),
        ('packed','packed'),
        ('on a way', 'on a way'),
        ('delivered', 'delivered')
    )
    status = models.CharField(max_length=10, blank=True, null=True, choices=STATUS, default='paid')
    order_date = models.DateTimeField(auto_now_add=True, blank=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    farmer_confirmation = models.IntegerField(blank=True, null=True)
    buyer_confirmation = models.IntegerField(blank=True, null=True)

