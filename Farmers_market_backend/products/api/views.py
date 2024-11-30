from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from products.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, ProductFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework import mixins



class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)  # Enable Django filter
    filterset_class = ProductFilter  # Apply the ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price_min', 'price_max', 'quantity_min', 'quantity_max', 'category', 'subcategory']

    # creating a product
    # route = POST products/
    def create(self, request):
        product_data = request.data
        serializer = self.get_serializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Product created"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # getting a specific product
    # route = GET products/<id>
    def retrieve(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    # updating a product
    # route = PUT products/<id>
    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Product was changed"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Где это работает?
    # updating product partially
    # route = PATCH products/<id>
    # def partial_update(self, request, pk=None):
    #
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = self.get_serializer(product, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deleting a product
    # route = DELETE products/<id>
    def destroy(self, request, pk=None):

        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"success": "Product was deleted succesfully"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['patch'], url_path='update-stock')
    def update_stock(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        new_quantity = request.data.get("quantity", None)

        if new_quantity is not None and isinstance(new_quantity, int):
            product.quantity = new_quantity
            product.save()
            return Response({"message": "Stock updated"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        threshold = request.query_params.get('threshold', 10)
        low_stock_products = Product.objects.filter(quantity__lte=threshold)
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
