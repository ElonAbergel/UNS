from django.db import models

# Create your models here.
class User(models.Model):
    Passport = models.IntegerField
    Public_key_Trust_Node = models.IntegerField
    Private_key_User = models.IntegerField
    website_name = models.CharField(max_length=500)
    