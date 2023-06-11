from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField
    email = models.CharField
    password = models.CharField 
    passport = models.CharField
    trustNode = models.CharField
    