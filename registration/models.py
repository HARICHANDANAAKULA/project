from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import re


class User(AbstractUser):
    drive = models.OneToOneField('drive_data.Folder', on_delete=models.SET_NULL, null=True, related_name='drive_user')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, blank=True, unique=True, default="h@gmail.com")
    email_confirmation = models.BooleanField(null=True, blank=True, default =False)
    pass
    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=instance)
