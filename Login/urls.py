
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path("login",views.login, name='login'),
    path("login_api",views.login_api, name='login_api'),

]
