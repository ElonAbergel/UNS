from django.db import models

# Create your models here.
class User(models.Model):
    Passport = models.CharField(max_length=500)
    Public_key_user = models.CharField(max_length=500)
    Private_key_TrustNode = models.CharField(max_length=500)