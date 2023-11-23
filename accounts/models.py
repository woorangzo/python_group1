from django.db import models


class Member(models.Model):
    member_id = models.CharField(max_length=100,primary_key=True)
    member_pw = models.CharField(max_length=100)
    member_repw = models.CharField(max_length=100,default='')
    phone = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True)
    jumin = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
