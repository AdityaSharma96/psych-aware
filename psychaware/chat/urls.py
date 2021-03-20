from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatroom_<int:appointment_id>_<str:room_name>', views.chat_page, name='chat_page'),
]