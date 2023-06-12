from django.urls import path, include
from . import views



urlpatterns = [
    path('user_keys/',views.TrustNodeUserSybil_keys,name='register')
    
]