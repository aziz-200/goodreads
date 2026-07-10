from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to = 'profile_pic', blank = True, default='profile_default_pic.jpg')
