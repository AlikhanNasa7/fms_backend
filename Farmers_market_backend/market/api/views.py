from django.shortcuts import render
from rest_framework import viewsets
from users.models import Farmer, Buyer
#from users.api.serializers import FarmerRegistrationSerializer, BuyerRegistrationSerializer
from users.api.permissions import IsFarmer, IsBuyer
from market.models import Farm
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import FarmRankSerializer, FarmSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()
        

    def create(self, request):

        farmer_id = request.user.user_id
        farmer = Farmer.objects.get(user=farmer_id)
        print(request.data)

        farm = Farm(
            farm_name=request.data.get('farm_name'),
            description=request.data.get('description'),
            farmer_id = farmer,
            farm_size = request.data.get('farm_size'),
            farm_location = request.data.get('farm_location')
        )
        farm.save()

        image_files = self.request.FILES.getlist('image_urls')
        print(image_files)

        if image_files:
            image_urls = []
            for image in image_files:
                file_name = f"farmer_images/{image.name}"
                file_path = default_storage.save(file_name, ContentFile(image.read()))
                print(file_path)
                
                image_url = f"{settings.MEDIA_URL}{file_path}"
                image_urls.append(image_url)

            print(image_urls)
            farm.image_urls = image_urls
            farm.save()


        serializer = self.get_serializer(farm)
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        farm = get_object_or_404(Farm, pk=pk)
        serializer = self.get_serializer(farm)
        return Response(serializer.data)

    # Update a specific farm
    def update(self, request, pk=None):
        farm = get_object_or_404(Farm, pk=pk)
        print(farm, request.data)
        serializer = self.get_serializer(farm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Farm updated successfully"}, status=status.HTTP_202_ACCEPTED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a specific farm
    def destroy(self, request, pk=None):
        farm = get_object_or_404(Farm, pk=pk)
        farm.delete()
        return Response({"success": "Farm deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='farmer')
    def farmer_farms(self, request):
        farmer = request.user.user_id
        farmer_farms = Farm.objects.filter(farmer_id=farmer)
        serializer = self.get_serializer(farmer_farms, many=True)
        return Response(serializer.data)

# class FarmerViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsFarmer]
#     serializer_class = FarmerRegistrationSerializer

#     def get_queryset(self):
#         return Farmer.objects.filter(id=self.request.user.id)


# class BuyerViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsBuyer]
#     serializer_class = BuyerRegistrationSerializer

#     def get_queryset(self):
#         return Buyer.objects.filter(id=self.request.user.id)
