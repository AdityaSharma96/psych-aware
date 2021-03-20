from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NameForm
from schedule.models import Appointment

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def index(request):
    return redirect('home')
    # if request.method == 'POST':
    #     userform = NameForm(request.POST)
    #     roomname=userform.data['roomname']
    #     print(userform.data)
    #     return render(request, 'chatroom.html', {
    #     'room_name': roomname
    # })
    # else:
    #     myform = NameForm()
    #     return render(request, 'index.html', {'form': myform})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def chat_page(request,appointment_id,room_name):
    appointment = Appointment.objects.get(appointment_id=appointment_id)
    expert_profile = appointment.expert_profile
    client_profile = appointment.client_profile
    return render(request, 'chatroom.html', {'room_name':room_name, 'expert_profile':expert_profile, 'client_profile':client_profile})

