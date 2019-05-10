from django.urls import path
from django.views.generic import TemplateView

from bugtracker.api.errors import Error
from bugtracker.api.login import Login
from bugtracker.api.logout import Logout
from bugtracker.api.registration import UserRegistration

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('error_log/', Error.as_view(), name='error_log'),
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', Login.as_view(), name='user_login'),
    path('logout/', Logout.as_view(), name='user_logout'),
]