from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views
#
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html')),
    path('logout', auth_views.LogoutView.as_view()),
    path('', views.index, name='index'),
]