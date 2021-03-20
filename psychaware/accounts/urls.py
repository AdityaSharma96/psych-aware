from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('user_register',views.clientRegister, name="user_register"),
    path('expert_register',views.expertRegister, name="expert_register"),
    path('profile',views.profile, name="profile"),
    path('review/write',views.write_review, name="write_review"),
    # path('testView',views.testView, name="testView"),
]
