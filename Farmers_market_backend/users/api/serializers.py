import datetime
from django.contrib.auth.models import User
from pip._vendor.requests.models import Response
from rest_framework import serializers

from users.models import Farmer, Buyer, CustomUser

# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Admin
#         fields = ['password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['username', 'email', 'role']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.role == 'Farmer':
            representation['profile'] = FarmerSerializer(instance.farmer_profile).data
        elif instance.role == 'Buyer':
            representation['profile'] = BuyerSerializer(instance.buyer_profile).data
        else:
            representation['profile'] = None  # Fallback for unknown roles or missing profiles

        return representation


class FarmerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Farmer
        fields = "__all__"


class BuyerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Buyer
        fields = "__all__"


