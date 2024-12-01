from django.urls import path, include
from carts.api.views import CartViewset
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# Register the viewset with the router
# This will generate routes for ProductViewSet actions
# /products/
router.register(r'', CartViewset, basename='carts')

# Include the router-generated URLs
urlpatterns = [
    path('', include(router.urls)),
]