from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
from users.models import CustomUser, Farmer, Buyer
from django.core.validators import MaxValueValidator, MinValueValidator


class Farm(models.Model):
    farm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36)
    farmer_id = models.ForeignKey(Farmer, models.CASCADE, related_name="farms")
    farm_name = models.CharField(max_length=255)
    farm_size = models.FloatField()
    farm_location = models.TextField()
    image_urls = models.JSONField(default=list, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)  # This will hold the rejection reason, if any.
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.farm_name}: {self.farm_location} ({self.farmer_id.user.first_name})"
  

class FarmRank(models.Model):
    rank_id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36)
    farm_id = models.ForeignKey(Farm, models.CASCADE, related_name="rank")
    value = models.DecimalField(decimal_places=1, max_digits=2,validators=[MaxValueValidator(5), MinValueValidator(0)])
    description = models.TextField(blank=True)
    buyer_id = models.ForeignKey(Buyer, models.DO_NOTHING, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)



class FarmAnalytics(models.Model):
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE, related_name='analytics')
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    products_sold = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    top_selling_product = models.CharField(max_length=255, blank=True, null=True) 
    repeat_buyers_count = models.PositiveIntegerField(default=0)
    monthly_sales = models.JSONField(default=dict)
    gross_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    completed_orders_count = models.PositiveIntegerField(default=0)  
    cancelled_orders_count = models.PositiveIntegerField(default=0) 
    buyer_feedback_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Analytics for {self.farm.name}"