from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, Order, Delivery

@receiver(post_save, sender=OrderItem)
def create_delivery(sender, instance, created, **kwargs):
    if created:
        # Construct the primary key for the Delivery
        delivery_pk = f'{instance.order_id.pk}_{instance.farm_id.pk}'

        # Use get_or_create to avoid DoesNotExist error
        delivery, delivery_created = Delivery.objects.get_or_create(
            pk=delivery_pk,
            defaults={
                'delivery_method': 'courier',  # Default delivery method
                'status': 'paid',  # Default status
                'farmer_confirmation': None,  # Defaults to None
                'buyer_confirmation': None,  # Defaults to None
            }
        )

        # Optionally, log or perform further actions
        if delivery_created:
            print(f"Delivery created with ID: {delivery_pk}")