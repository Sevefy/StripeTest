
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item
import stripe
from .exception import exception_stripe

@receiver(post_save, sender=Item)
@exception_stripe
def post_create_item(sender, instance: Item, created, **kwargs):
    if created:
        stripe.Product.create(name=instance.name, description=instance.description)
        
# TODO Также можно добавить удаление и модификацию