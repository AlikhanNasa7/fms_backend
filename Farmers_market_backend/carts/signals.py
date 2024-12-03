from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Buyer
from carts.models import Cart

@receiver(post_save, sender=Buyer)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(buyer=instance)