from django.urls import path, re_path

from . import views

urlpatterns = [
     path('website_keys/', views.TrustNodeWebsiteSybil_keys,name='register_website_keys'),
     path('message_Nonce/', views.TrustNodeWebsiteSybil_message,name='register_message_Nonce'),
]