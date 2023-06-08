from django.urls import path, re_path

from . import views

urlpatterns = [
     path('', views.Trust_Node_Main),
]