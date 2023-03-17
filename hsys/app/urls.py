from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('register', views.register,name='register'),
    path('login', views.login,name='login'),
    path('mark', views.mark,name='mark'),
    path('logout', views.logout,name='logout'),
    path('video_feed', views.video_feed, name='video_feed'),
]