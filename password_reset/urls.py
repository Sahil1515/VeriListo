
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path("",views.password_reset,name='password_reset'),
    path('send_password_reset_mail',views.send_password_reset_mail,name='send_password_reset_mail'),

]