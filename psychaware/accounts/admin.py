from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client_Profile, Expert_Profile, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Client_Profile)
admin.site.register(Expert_Profile)
admin.site.register(Review)