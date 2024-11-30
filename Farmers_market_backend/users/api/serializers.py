import datetime
from django.contrib.auth.models import User
from pip._vendor.requests.models import Response
from rest_framework import serializers

from users.models import Farmer, Buyer, CustomUser
from market.models import Farm
import django_filters
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
    #rank = serializers.FloatField()

    class Meta:
        model = Farmer
        fields = "__all__"

    def get_rank(self, obj):
        user = obj.pk
        farms = Farm.obj



class BuyerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Buyer
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email','first_name', 'last_name','role', 'phone_number', 'password']
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data.get('username', ''),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
            role=validated_data.get('role'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class FarmerFilter(django_filters.FilterSet):
    years_of_experience = django_filters.NumberFilter(field_name='years_of_experience', lookup_expr='gte')
    specialization = django_filters.CharFilter(field_name='specialization', lookup_expr='icontains')  # Case-insensitive partial match
    total_farm_area = django_filters.NumberFilter(field_name='total_farm_area', lookup_expr='gte')
    average_performance = django_filters.NumberFilter(field_name='average_performance', lookup_expr='gte')
    
    
    
    class Meta:
        model = Farmer
        fields = ['years_of_experience', 'specialization', 'total_farm_area', 'average_performance']



