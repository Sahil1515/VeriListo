
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path("habits",views.habits, name='habits'),
    path("habit_days_completed_inc",views.habit_days_completed_inc, name='habit_days_completed_inc'),
    path("habits_ajax",views.habits_ajax, name='habits_ajax'),


]
