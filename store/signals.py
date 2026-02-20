from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Cart, Library


@receiver(post_save, sender=User)
def create_user_data(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        Library.objects.create(user=instance)
