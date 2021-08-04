from django.db import models
from django.db.models.fields import TimeField, related, TextField
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Userdata(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.name

class Entry(models.Model):
    uid = models.TextField(max_length=16)
    createdtime = models.DateField()
    entry = models.CharField(max_length=1)
    
    def __str__(self):
        return self.name