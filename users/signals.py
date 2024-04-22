from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings

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

        SUBJECT = "Welcome to DevSearch"
        MESSAGE = "We are excited to have you here with us. Enjoy your stay!"

        # Send email to new user
        send_mail(
            SUBJECT,
            MESSAGE,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
    return

@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    return

@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    return
