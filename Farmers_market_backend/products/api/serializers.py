from rest_framework import serializers
from products.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    image_urls = serializers.ListField(child=serializers.URLField(), required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['product_id', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
