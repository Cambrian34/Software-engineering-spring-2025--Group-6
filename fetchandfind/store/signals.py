from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Product, AdminLog

"""
@receiver(post_save, sender=Product)
def log_product_create_or_update(sender, instance, created, **kwargs):
    
    user = None
    if instance.pk:  # If the product already exists, it's an update
        user = kwargs.get('user')  # Ensure the 'user' is passed with the signal

    if created:
        AdminLog.objects.create(
            admin=user,  # Log the current user
            action='created',
            content_object=instance
        )
    else:
        AdminLog.objects.create(
            admin=user,  # Log the current user
            action='updated',
            content_object=instance
        )


@receiver(post_delete, sender=Product)
def log_product_delete(sender, instance, **kwargs):
    user = kwargs.get('user')  # Capture the current user
    AdminLog.objects.create(
        admin=user,
        action='deleted',
        content_object=instance
    )
"""