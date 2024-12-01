
from django.urls import path, include
from .views import FarmViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Register the FarmViewSet and FarmerFarmViewSet
router.register(r'', FarmViewSet, basename='farms')  # For farms  # For farmer-specific farms

urlpatterns = [
    path('', include(router.urls))
]