from django.urls import path, re_path
from asgiref.sync import async_to_sync, sync_to_async
from . import views

urlpatterns = [
    path('register_user/', views.register_view, name='register'),
    path('token/', views.get_csrf_token, name='get_csrf_token'),

    # path('/', views.login_page),
    
]

