from django.urls import path

from account.api.views import *

from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('signup', views.SignUpAPI, name='signup-api'),
    path('signin', obtain_auth_token, name='signin-api')
]