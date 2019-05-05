from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
#
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    path('logout/', auth_views.LogoutView.as_view()),  # Fix it later
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
]