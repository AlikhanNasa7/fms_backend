from rest_framework import serializers
from users.models import Farmer, Buyer, CustomUser

# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Admin
#         fields = ['password']

class ProfileSerializer(serializers.ModelSerializer):
    # profile_data = serializers.SerializerMethodField()

    class Meta: 
        model = CustomUser
        exclude = ["password"]
    
    def get_profile_data(self, obj):
        if obj.role == "farmer":
            return FarmerSerializer(obj).data
        elif obj.role=="buyer": 
            return BuyerSerializer(obj).data
        # else:
        #     return AdminSerializer(obj).data


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
