from django.urls import path, include
from . import views



urlpatterns = [
    path('user_keys/',views.TrustNodeUserSybil_keys,name='register_The_KEYS'),
    path('message_send/',views.TrustNodeUserSybil_message,name='register_Message_Sending')
    
]