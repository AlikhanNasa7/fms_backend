from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from products.models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, ProductFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsFarmerOwner
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from market.models import Farm
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class FarmerProductsList(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFarmerOwner]

    def get_queryset(self, request):
        farmer_id = request.user.user_id
        return Product.objects.filter(farm_id__farmer_id=farmer_id)


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)  # Enable Django filter
    filterset_class = ProductFilter  # Apply the ProductFilter
    parser_classes = [MultiPartParser, FormParser]
    search_fields = ['name', 'description']
    ordering_fields = ['price_min', 'price_max', 'quantity_min', 'quantity_max', 'category', 'subcategory']

    # creating a product
    # route = POST products/
    def create(self, request):
        category_name = request.data.get('category')
        subcategory_name = request.data.get('sub_category')

        category = Category.objects.get(name=category_name) if category_name else None
        subcategory = SubCategory.objects.get(name=subcategory_name) if subcategory_name else None


        farm = Farm.objects.get(farm_id=request.data.get('farm_id'))
        print(request.data)

        print(request.data.get('image_urls'))
        product = Product(
            name=request.data.get('name'),
            farm_id=farm,
            category=category,
            subcategory=subcategory,
            price=request.data.get('price'),
            quantity=request.data.get('quantity'),
            unit_name=request.data.get('unit'),
            description=request.data.get('description'),
        )
        product.save()

        image_files = self.request.FILES.getlist('image_urls')
        print(image_files)

        if image_files:
            image_urls = []

            # Loop through the files and upload them to S3
            for image in image_files:
                # Save the image to S3
                file_name = f"product_images/{image.name}"  # You can customize this path
                file_path = default_storage.save(file_name, ContentFile(image.read()))

                # Get the URL of the uploaded file
                image_url = default_storage.url(file_path)
                image_urls.append(image_url)

            # Update the product with the URLs of the images
            product.image_urls = image_urls
            product.save()


        # Use the serializer to return the response
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=201)

    # getting a specific product
    # route = GET products/<id>
    def retrieve(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    # updating a product
    # route = PUT products/<id>
    def update(self, request, pk=None):
        instance = get_object_or_404(Product, pk=pk)
        category_name = request.data.get('category')
        subcategory_name = request.data.get('sub_category')

        category = Category.objects.get(name=category_name) if category_name else instance.category
        subcategory = SubCategory.objects.get(name=subcategory_name) if subcategory_name else instance.subcategory

        # If category and subcategory were passed as IDs, use those instead
        if not category and request.data.get('category'):
            category = Category.objects.get(id=request.data.get('category'))
        if not subcategory and request.data.get('sub_category'):
            subcategory = SubCategory.objects.get(id=request.data.get('sub_category'))

        # Get farm from farm_id
        farm = Farm.objects.get(farm_id=request.data.get('farm_id'))

        # Update the instance fields with the new data
        instance.name = request.data.get('name', instance.name)
        instance.farm_id = farm
        instance.category = category
        instance.subcategory = subcategory
        instance.price = request.data.get('price', instance.price)
        instance.quantity = request.data.get('quantity', instance.quantity)
        instance.unit_name = request.data.get('unit_name', instance.unit_name)
        instance.description = request.data.get('description', instance.description)
        instance.image_urls = request.data.get('image_urls', instance.image_urls)

        instance.save()

        # Serialize the updated product
        serializer = ProductSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['get'], url_path='farmer')
    def get_farmer_farms(self, request):
        farmer_id = self.request.user.user_id
        products = Product.objects.filter(farm_id__farmer_id=farmer_id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='create-product')
    def farmer_farms_names(self, request):
        farmer = request.user.user_id
        farmer_farms = Farm.objects.filter(farmer_id=farmer)
        farms = farmer_farms.values('farm_id', 'farm_name')
        farms_list = list(farms)

        products = Product.objects.values('category', 'subcategory').distinct()
        categories = dict()

        for product in products:
            if product['category'] not in categories:
                categories[product['category']] = []
            categories[product['category']].append(product['subcategory'])

        return JsonResponse({"farms": farms_list, 'categories': categories})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
