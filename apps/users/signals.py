from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.users.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check if profile already exists to avoid duplicates
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)
