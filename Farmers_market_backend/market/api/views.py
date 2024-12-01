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

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()
        

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Farm created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
