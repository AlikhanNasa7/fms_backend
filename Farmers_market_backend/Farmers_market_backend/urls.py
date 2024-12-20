from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.api.urls')),
    path('products/', include('products.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('farms/', include('market.api.urls')),
    path('api/', include('users.api.urls')),
    path('carts/', include('carts.api.urls')),

    path('orders/', include('orders.api.urls')),
    path('chat/', include('chat.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
