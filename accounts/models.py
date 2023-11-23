from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)