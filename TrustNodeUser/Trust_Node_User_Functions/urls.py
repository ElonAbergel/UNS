from django.urls import path, include
from . import views



urlpatterns = [
    path('user_keys/',views.TrustNodeUserSybil,name='register')
    
]