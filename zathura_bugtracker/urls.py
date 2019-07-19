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
from rest_framework_swagger.views import get_swagger_view

from zathura_bugtracker.settings import DEBUG

schema_view = get_swagger_view(title='Zathura Bugtracker API')

urlpatterns = [
    path('zathura/', include('bugtracker.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('bugtracker.urls'), name='home'),
]

if DEBUG:
    # Only add certain urls if it's in Debug mode.
    urlpatterns.append(
        path('admin/', admin.site.urls),
    )
    urlpatterns.append(
        path("swagger/", schema_view),
    )