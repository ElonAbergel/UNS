from django.db import models

# Create your models here.

class Dealer(models.Model):
    Passport = models.IntegerField(max_length=500)
    Public_key_user = models.IntegerField(max_length=500)
    Private_key_user = models.IntegerField(max_length=500)
    Public_key_TrustNode_Website = models.IntegerField(max_length=500)
    Private_key_TrustNode_Website = models.IntegerField(max_length=500)
    Dealer_Key = models.IntegerField(max_length=500)





    