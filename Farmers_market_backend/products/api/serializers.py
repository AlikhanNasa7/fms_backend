from rest_framework import serializers
from products.models import Product, Category, SubCategory
import django_filters

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


class ProductFilter(django_filters.FilterSet):
    # Price range filtering (greater than or equal to)
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Quantity range filtering (greater than or equal to)
    quantity_min = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity_max = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte')

    # Filtering by category and subcategory using exact match
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), field_name='category')
    subcategory = django_filters.ModelChoiceFilter(queryset=SubCategory.objects.all(), field_name='subcategory')

    # # Filtering by availability (True or False)
    is_available = django_filters.BooleanFilter(field_name='is_available')

    # Name search (case-insensitive match)
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # Description search (case-insensitive match)
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'quantity_min', 'quantity_max', 'is_available', 'name', 'description', 'category', 'subcategory']
