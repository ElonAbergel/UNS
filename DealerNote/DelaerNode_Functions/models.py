from django.db import models

# Create your models here.

class Dealer(models.Model):
    Passport = models.IntegerField
    Public_key_user = models.IntegerField
    Private_key_user = models.IntegerField
    Public_key_TrustNode_Website = models.IntegerField
    Private_key_TrustNode_Website = models.IntegerField
    Dealer_Key = models.IntegerField
    Website = models.CharField(max_length=500)





    