from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    pseudo = models.CharField(max_length=254, blank=True)
    phone = models.CharField(max_length=254, blank=True)

class Tutor(models.Model):
    firstname = models.CharField(max_length=254)
    lastname = models.CharField(max_length=254)
    phone = models.CharField(max_length=254)
    job = models.CharField(max_length=254)

class Event(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    begin = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)
    youtube = models.URLField(blank=True)
    manager = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):
        return self.title
