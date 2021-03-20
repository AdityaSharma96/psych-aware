from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('appointment', views.appointment_view, name="appointment_view"),
    path('expert_appointment', views.expert_appointment_view, name="expert_appointment_view"),
    path('response/<int:appointment_id>', views.response_view, name="response_view"),
    path('expert_response/<int:appointment_id>', views.expert_response_view, name="expert_response_view"),
    path('get_appointment/<int:profile_id>', views.get_appointment, name="get_appointment"),
]
