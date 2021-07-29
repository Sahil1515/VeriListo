
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path("",views.index),
    path("delete_api",views.delete_api, name='delete_api'),
    path("updateClass_api",views.updateClass_api, name='updateClass_api'),
    # path("insert_task_api",views.insert_task_api, name='insert_task_api'),

    
]
