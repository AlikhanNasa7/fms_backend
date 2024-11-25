from django.db import models
from market.models import Farm
from users.models import Farmer
from django.utils import timezone
import uuid

class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)



class SubCategory(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    category = models.ForeignKey(Category, models.CASCADE)


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36)
    farm_id = models.ForeignKey(Farm, models.CASCADE)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_name = models.CharField(max_length=20, choices=[
        ('kg', 'kg'),
        ('pcs', 'pcs'),
        ('litres', 'litres')
    ], default='kg')
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=True)
    image_urls = models.JSONField(blank=True, null=True)
    is_available = models.BooleanField(blank=True, null=True, default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.name}: {self.farm_id.farm_name}"
