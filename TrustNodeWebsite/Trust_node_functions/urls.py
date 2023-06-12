from django.urls import path, re_path

from . import views

urlpatterns = [
     path('website_keys/', views.TrustNodeWebsiteSybil_keys,name='register'),
]