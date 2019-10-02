"""zathura_bugtracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from user.apis.user_authentication import UserRegistration, UserLogin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from organization.apis.org import Org
from projects.apis.project import ProjectCRUD
from token_manager.apis.token import ProjectToken
from error_logger.apis.ErrorLogZathura import ErrorLogZathura
from error_logger.apis.VerboseLogZathura import VerboseLogZathura
from ping_app.views import Ping

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register/', UserRegistration.as_view()),
    path('user/login/', UserLogin.as_view()),
    path('org/create/', Org.as_view()),
    path('project/', ProjectCRUD.as_view()),
    path('project/token/', ProjectToken.as_view()),
    path('project/error/log/', ErrorLogZathura.as_view()),
    path('project/verbose/log/', VerboseLogZathura.as_view()),
    path('ping/add/', Ping.as_view()),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# urlpatterns = [
#     path('zathura/', include('bugtracker.urls')),
# ]
