from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .models import Appointment
from accounts.models import Expert_Profile, Client_Profile
import random
import datetime


from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def get_appointment(request,profile_id):
    if request.method == "POST":
        client_profile = request.user.client_profile
        expert_profile = Expert_Profile.objects.get(profile_id=int(profile_id))
        appointment = Appointment(client_profile=client_profile,
        expert_profile=expert_profile,
        datetime= None,
        client_acknowledgement='NA',
        expert_acknowledgement='NA',
        chat_room='NA')
        appointment.save()
    return redirect('profile')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def appointment_view(request):

    follow_list = Appointment.objects.filter(client_profile=request.user.client_profile, client_acknowledgement='NA')
    scheduled_list = Appointment.objects.exclude(client_acknowledgement='NA').filter(client_profile=request.user.client_profile)

    return render(request, 'accounts/viewAppointment.html',{'follow_list':follow_list, 'scheduled_list':scheduled_list})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def expert_appointment_view(request):
    follow_list = Appointment.objects.filter(expert_profile=request.user.expert_profile, expert_acknowledgement='NA')
    scheduled_list = Appointment.objects.filter(expert_profile=request.user.expert_profile, expert_acknowledgement='A', client_acknowledgement='A')

    return render(request, 'accounts/expertViewAppointment.html', {'follow_list':follow_list, 'scheduled_list':scheduled_list})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def response_view(request, appointment_id):
    if request.method == "POST":
        appointment = Appointment.objects.get(appointment_id=appointment_id)
        if 'confirm-response' in request.POST:
            # Set Client Ack To 'A'
            appointment.client_acknowledgement = 'A'

            # Generate Random Hash
            hash = random.getrandbits(32)
            chat_url = 'chat/chatroom_' + str(appointment_id) + '_' + str(hash)
            appointment.chat_room = chat_url
        else:
            # Set Client Ack To 'R'
            appointment.client_acknowledgement = 'R'
        appointment.save()
    return redirect('appointment_view')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def expert_response_view(request, appointment_id):
    if request.method == "POST":
        appointment = Appointment.objects.get(appointment_id=appointment_id)
        if 'accept-response' in request.POST:
            appointment_dateresp = request.POST.get('appointment_datetime','')
            # Set Client Ack To 'A'
            appointment.expert_acknowledgement = 'A'
            appointment.datetime = appointment_dateresp
        else:
            # Set Client Ack To 'R'
            appointment.expert_acknowledgement = 'R'
        appointment.save()
    return redirect('expert_appointment_view')