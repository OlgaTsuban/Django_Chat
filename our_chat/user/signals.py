from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# created for profile creation
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    try:
        profile = instance.profile
    except Profile.DoesNotExist:
        profile = None

    if created or profile is None:
        print("Creating profile for user:", instance)
        Profile.objects.create(user=instance)
    else:
        print("Updating profile for user:", instance)
        instance.profile.save()

