from django.db import models

# Create your models here.
class User(models.Model):
    Passport = models.CharField(max_length=500)
    Public_key_Trust_Node = models.CharField(max_length=500)
    Private_key_User = models.CharField(max_length=500)
    website_name = models.CharField(max_length=500)
    