
from django.urls import path, include
from .views import ProductViewSet, FarmerProductsList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Register the viewset with the router
# This will generate routes for ProductViewSet actions
# /products/
router.register(r'', ProductViewSet, basename='product')
router.register(r'farmer', FarmerProductsList, basename='farmer-product')

# Include the router-generated URLs
urlpatterns = [
    path('', include(router.urls)),
]