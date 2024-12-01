from rest_framework import serializers
from market.models import Farm, FarmRank
from users.models import Farmer

class FarmSerializer(serializers.ModelSerializer):
    farmer = serializers.CharField(source='farmer_id.user', read_only=True)
    product_categories = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Farm
        fields = ['farm_id', 'farmer_id', 'farm_name', 'farm_size', 'farm_location', 'image_urls', 'farmer', 'product_categories', 'units', 'products_count', 'description']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('request').method in ['PUT', 'PATCH', 'POST']:
            self.fields['image_urls'].required = False 
            self.fields['farmer_id'].required = False
        else:
            self.fields['image_urls'].required = True

    def create(self, validated_data):
        farmer_id = self.context['request'].user.user_id
        farmer = Farmer.objects.get(pk=farmer_id)
        validated_data['farmer_id'] = farmer

        return Farm.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        print(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def get_product_categories(self, obj):
        farm_categories = obj.products.values('category').distinct()

        return [category['category'] for category in farm_categories]
    
    def get_products_count(self, obj):
        farm_products_count = obj.products.count()

        return farm_products_count
    
    def get_units(self, obj):
        farm_units = obj.products.values('unit_name').distinct()

        return [unit['unit_name'] for unit in farm_units]

        



class FarmRankSerializer(serializers.ModelSerializer):
    farm_name = serializers.CharField(source='farm_id.farm_name', read_only=True)
    buyer_name = serializers.CharField(source='buyer_id.user.first_name', read_only=True)

    class Meta:
        model = FarmRank
        fields = ['rank_id', 'farm_id', 'value', 'description', 'buyer_id', 'created_at', 'farm_name', 'buyer_name']
