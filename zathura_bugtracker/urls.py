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

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from error_logger.apis.ErrorLogZathura import ErrorLogZathura
from error_logger.apis.VerboseLogZathura import VerboseLogZathura
from frontend._views.dashboard import DashboardView
from frontend._views.index import Index
from frontend._views.logout import LogoutView
from frontend._views.profile import ProfileView
from frontend._views.project import ProjectView
from frontend._views.team import TeamView
from frontend._views.error_log import ErrorLogView
from ping_app.apis.ping import Ping
from projects.apis.project import ProjectCRUD
from team.apis.team_manager import TeamManager
from token_manager.apis.token import ProjectToken
from user.apis.user_authentication import UserLogin, UserRegistration

urlpatterns = [
    # ---------------------------------
    # Front End
    # ---------------------------------
    path('', Index.as_view(), name="index"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('project/<project_id>/', ProjectView.as_view(), name="project"),
    path('team/<team_id>/', TeamView.as_view(), name="team"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('errors/', ErrorLogView.as_view(), name="error_log"),


    path('admin/', admin.site.urls),
    path('user/register/', UserRegistration.as_view(), name="register"),
    path('user/login/', UserLogin.as_view(), name="login"),
    path('team/', TeamManager.as_view(), name="team_create"),
    path('project/', ProjectCRUD.as_view(), name="project_create"),
    path('token/generate/', ProjectToken.as_view(),  name="token_generate"),
    path('log/error/', ErrorLogZathura.as_view()),
    path('log/verbose/', VerboseLogZathura.as_view()),
    path('ping/add/', Ping.as_view(), name="ping_create"),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

# urlpatterns = [
#     path('zathura/', include('bugtracker.urls')),
# ]
