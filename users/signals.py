from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User

# Decorators
from django.dispatch import receiver

# Signals


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user, username=user.username, email=user.email, name=user.first_name
        )
    return


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    return
