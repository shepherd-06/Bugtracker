from django.urls import path
from django.views.generic import TemplateView

from bugtracker.api.errors_log import ErrorLog
from bugtracker.api.login import Login
from bugtracker.api.logout import Logout
from bugtracker.api.organization import Org
from bugtracker.api.project import Project
from bugtracker.api.project_token import ProjectTokenCRUD
from bugtracker.api.registration import UserRegistration
from bugtracker.api.token_renew import UserTokenRenew

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('error_log/', ErrorLog.as_view(), name='error_log'),
    path('error_log/<str: error_pk>/', ErrorLog.as_view()),
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', Login.as_view(), name='user_login'),
    path('logout/', Logout.as_view(), name='user_logout'),
    path('user_renew/', UserTokenRenew.as_view(), name='user_token_renew'),
    path('project/', Project.as_view(), name='project_cr'),
    path('project/<str:pk>/', Project.as_view(), name='project_update_delete'),
    path('org/', Org.as_view(), name='organization'),
    path('org/<str:pk>/', Org.as_view(), name='organization_update_delete'),
    path('project_token_renew/', ProjectTokenCRUD.as_view()),
    path('project_token_renew/<str:project_token>/', ProjectTokenCRUD.as_view()),
]