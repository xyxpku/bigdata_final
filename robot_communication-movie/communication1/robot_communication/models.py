from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Sys_user(models.Model):
    '''用户信息'''

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.EmailField()

class Communication(models.Model):
    # '''所有微博'''
    com_type=models.CharField(max_length=140)
    com_content= models.CharField(max_length=14000)
    date = models.DateTimeField(auto_now_add=True)

class Communication_2(models.Model):
    # '''所有微博'''
    com_type=models.CharField(max_length=140)
    com_content= models.CharField(max_length=14000)
    date = models.DateTimeField(auto_now_add=True)