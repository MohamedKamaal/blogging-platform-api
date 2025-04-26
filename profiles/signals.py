# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a Profile instance automatically when a new User is created.

    Args:
        sender: The model class that sent the signal (User).
        instance: The actual instance of the User that was saved.
        created (bool): Boolean indicating whether this is a new instance being created.
        **kwargs: Additional keyword arguments passed with the signal.
    """
    if created:
        Profile.objects.create(user=instance)