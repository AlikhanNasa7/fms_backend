from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
from users.models import CustomUser, Farmer, Buyer
from django.core.validators import MaxValueValidator, MinValueValidator

class Farm(models.Model):
    farm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36)
    farmer_id = models.ForeignKey(Farmer, models.CASCADE)
    farm_name = models.CharField(max_length=255)
    farm_size = models.FloatField()
    farm_location = models.TextField()
    image_urls = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.farm_name}: {self.farm_location} ({self.farmer_id.user.first_name})"
    

class FarmRank(models.Model):
    rank_id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=36)
    farm_id = models.ForeignKey(Farm, models.CASCADE)
    value = models.DecimalField(decimal_places=1, max_digits=2,validators=[MaxValueValidator(5), MinValueValidator(0)])
    description = models.TextField(blank=True)
    buyer_id = models.ForeignKey(Buyer, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)



