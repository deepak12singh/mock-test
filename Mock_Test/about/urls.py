# users/urls.py
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from .views import about


urlpatterns = [
    path('about/', about ,name='about'),
]