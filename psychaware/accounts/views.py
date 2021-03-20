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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        user = authenticate(email=email, password=password)
        print('USER: ', str(user),"Email: ",email, "password: ", password)
        if user is not None and user.is_active:
            # Login Successfull
            login(request, user)
            return redirect('profile')
        else:
            # Login Unsuccessfull , Show Same Page With Error
            return render(request, 'accounts/login.html', {'loginStatus':"Incorrect Credentials."})
    else:
        if request.user.is_authenticated:
            # If user is already logged in, send to home
            return redirect('home')
        # Display Login Page
        return render(request,'accounts/login.html', {'loginStatus':'OK'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def expertRegister(request):
    if request.method=="POST":
        user_form = CustomUserCreationForm(request.POST)
        logError = ''

        user_email = request.POST.get('email', '')
        user_password = request.POST.get('password1', '')
        # Check if the email is already in database
        if User.objects.filter(email=str(user_email)).exists():
            logError += 'Email Already Exists In Database.\n'
        
        # Password validation using regex
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        compiledReg = re.compile(reg)
        if not re.search(compiledReg, user_password):
            logError += 'Password must contain between 8-32 characters including atleast one digit, alphabet, capital and symbol each.\n'
        
        
        if logError != '':
            # That is if error exists in form data, send error
            return render(request, 'accounts/clientRegistration.html' , {'registerStatus':'error', 'logError':logError})

        if user_form.is_valid():
            # Creating Basic User Account
            user = user_form.save()

            # Gender and Form Radio Buttons Mapping
            gender_options = {'1':'Male', '2':'Female', '3':'Other'}

            # Extracting Additional Data From Registration Form
            name = request.POST.get('name', '')
            dob = request.POST.get('date', '')
            contact_number = request.POST.get('mobile', '')
            address = request.POST.get('address', '')
            qualification = request.POST.get('qualification', '')
            bio = request.POST.get('bio', '')
            gender_choice = request.POST.get('gender', '')
            gender = gender_options[gender_choice]
            user_type = 'Expert'

            # Create Complete Expert_Profile From Basic User Account
            expert_profile = Expert_Profile(name=name,
            date_of_birth=dob,
            contact_number=contact_number,
            address=address,
            gender=gender,
            qualification=qualification,
            bio=bio)

            expert_profile.save()

            # Link User Account To Expert_Profile Using One To One Field
            user.expert_profile = expert_profile
            user.user_type = user_type
            user.save()

            # Return To Registration Success Page
            return render(request,'accounts/registrationSuccessful.html')
    else:
        return render(request,'accounts/expertRegistration.html', {'registerStatus':'OK'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def clientRegister(request):
    if request.method=="POST":
        user_form = CustomUserCreationForm(request.POST)
        logError = ''

        user_email = request.POST.get('email', '')
        user_password = request.POST.get('password1', '')
        # Check if the email is already in database
        if User.objects.filter(email=str(user_email)).exists():
            logError += 'Email Already Exists In Database.\n'
        
        # Password validation using regex
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        compiledReg = re.compile(reg)
        if not re.search(compiledReg, user_password):
            logError += 'Password must contain between 8-32 characters including atleast one digit, alphabet, capital and symbol each.\n'
        

        if logError != '':
            # That is if error exists in form data, send error
            return render(request, 'accounts/clientRegistration.html' , {'registerStatus':'error', 'logError':logError})

        if user_form.is_valid():            
            # Creating Basic User Account
            user = user_form.save()

            # Gender and Form Radio Buttons Mapping
            gender_options = {'1':'Male', '2':'Female', '3':'Other'}

            # Extracting Additional Data From Registration Form
            name = request.POST.get('name', '')
            dob = request.POST.get('date', '')
            contact_number = request.POST.get('mobile', '')
            address = request.POST.get('address', '')
            bio = request.POST.get('bio', '')
            gender_choice = request.POST.get('gender', '')
            gender = gender_options[gender_choice]
            user_type = 'Client'

            # Create Complete Expert_Profile From Basic User Account
            client_profile = Client_Profile(name=name,
            date_of_birth=dob,
            contact_number=contact_number,
            address=address,
            gender=gender,
            bio=bio)

            client_profile.save()

            # Link User Account To Expert_Profile Using One To One Field
            user.client_profile = client_profile
            user.user_type = user_type
            user.save()

            # Return To Registration Success Page
            return render(request,'accounts/registrationSuccessful.html')
    else:
        return render(request, 'accounts/clientRegistration.html' , {'registerStatus':'OK'})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    if not request.user.is_authenticated:
        # If the user is not logged in , send to home
        return redirect('home')
    logout(request)
    return render(request, 'accounts/logout.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def profile(request):
    if request.method == "POST":
        # Return To Something Went Wrong Page
        return None
    elif request.user.user_type == "Client":
        # Redirect To Client Profile Dashboard
        expert_list = Expert_Profile.objects.filter()
        print("expert_list", str(expert_list))
        client_profile = request.user.client_profile
        return render(request,'accounts/clientDashboard.html', {'client_profile': client_profile, 'expert_list':expert_list})

    elif request.user.user_type == "Expert":
        # Redirect To Expert Profile Dashboard
        expert_profile = request.user.expert_profile
        tag_list = blogModels.Blog_Tag.objects.all()
        #print(str(tag_list))

        # Find The Blogs Written By Logged In Expert
        blogs_written = blogModels.Blogpost.objects.filter(author=expert_profile)
        blogs_written_mod = []
        written_blogs_len = len(blogs_written)

        # Modify Blog Title
        for bg in blogs_written:
            blogs_written_mod.append([bg, bg.title.replace(" ", "_")])

        return render(request,'accounts/expertDashboard.html', {'expert_profile':expert_profile, 'tag_list':tag_list, 'blogs_written':blogs_written_mod, 'written_blogs_len':written_blogs_len})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='user_login')
def write_review(request):
    if request.method == "POST":
        review_content = request.POST.get('review_content','')
        try:
            # Check If Review Already Exists By This User
            review = Review.objects.get(author=request.user)
            review.content = review_content
            review.save()
        except:
            # If Review Is Not Present Create New Object In Database
            review = Review(author=request.user, content=review_content)
            review.save()
    return render(request,'accounts/reviewSuccessful.html')