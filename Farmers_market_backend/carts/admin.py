from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

