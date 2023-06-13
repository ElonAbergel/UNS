from django.db import models

# Create your models here.
class User(models.Model):
    Passport = models.IntegerField
    Public_key_Trust_Node = models.IntegerField
    private_key_Dealer_u = models.IntegerField
    website_name = models.CharField(max_length=500)
    Public_key_User= models.IntegerField
    