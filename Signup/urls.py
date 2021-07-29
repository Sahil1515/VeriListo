
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('signup',views.SignUp,name='signup'),
    path('send_otp',views.send_otp,name='send_otp'),
    path('check_user_api',views.check_user_api,name='check_user_api'),
    path('create_user_after_verification',views.create_user_after_verification,name='create_user_after_verification'),


    

]