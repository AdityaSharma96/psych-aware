from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import Expert_Profile, User, Client_Profile, Review
from django.contrib.auth import login, authenticate, logout
from blogs import models as blogModels
import re # for password validation
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.

def testView(request):
    return render(request, 'accounts/chatTest.html', {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    # Get all reviews from database
    review=Review.objects.all()
    return render(request,'accounts/home.html',{'reviews':review})