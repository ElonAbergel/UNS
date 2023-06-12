from django.db import models

# Create your models here.
class User(models.Model):
    Passport = models.IntegerField
    Public_key_user = models.IntegerField
    Private_key_TrustNode = models.IntegerField
    website_name = models.CharField(max_length=500)
    T1_nonce = models.IntegerField