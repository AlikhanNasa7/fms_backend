from django.urls import path, include
from orders.api.views import OrderViewset
from rest_framework.routers import DefaultRouter

from django.urls import path, include

router = DefaultRouter()

# Register the viewset with the router
# This will generate routes for ProductViewSet actions
# /products/
router.register(r'', OrderViewset, basename='carts')

# Include the router-generated URLs
urlpatterns = [
    path('', include(router.urls)),
]
