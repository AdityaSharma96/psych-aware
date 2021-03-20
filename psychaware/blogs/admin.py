from django.contrib import admin
from .models import Blogpost, Blog_Tag, Blogpost_Tag
# Register your models here.

admin.site.register(Blogpost)
admin.site.register(Blog_Tag)
admin.site.register(Blogpost_Tag)