from django.urls import path, re_path
from asgiref.sync import async_to_sync, sync_to_async
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register'),
    # path('login_user/', views.Register_or_Login, name='login'),
    path('token/', views.get_csrf_token, name='get_csrf_token'),

    # path('/', views.login_page),
    
]

