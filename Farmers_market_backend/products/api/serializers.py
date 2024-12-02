from rest_framework import serializers
from products.models import Product, Category, SubCategory
import django_filters
from django.db import models

class ProductSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()
    image_urls = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['product_id', 'updated_at']

    def get_farm_name(self, obj):
        farm_name = obj.farm_id.farm_name
        return farm_name

    def get_image_urls(self, obj):
        image_urls = obj.image_urls
        for i in range(len(image_urls)):
            image_urls[i] = 'http://127.0.0.1:8000' + image_urls[i]
        return image_urls


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductFilter(django_filters.FilterSet):
    # Price range filtering (greater than or equal to)
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', required=False)
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', required=False)

    # Quantity range filtering (greater than or equal to)
    quantity_min = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte', required=False)
    quantity_max = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte', required=False)

    # Filtering by category and subcategory using exact match
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', required=False)
    subcategory = django_filters.CharFilter(field_name='subcategory__name', lookup_expr='icontains', required=False)


    # # Filtering by availability (True or False)
    is_available = django_filters.BooleanFilter(field_name='is_available', required=False)

    # Name search (case-insensitive match)
    search = django_filters.CharFilter(method='filter_search', required=False)



    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'quantity_min', 'quantity_max', 'is_available', 'name', 'description', 'category', 'subcategory']


    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(name__icontains=value) | 
                models.Q(description__icontains=value)
            )
        return queryset
