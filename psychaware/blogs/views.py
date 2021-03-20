from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .models import Blogpost, Blogpost_Tag, Blog_Tag
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import random

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_url')
def blog_write(request):
    if request.method == "POST":
        # Blog Post Is Submitted
        blog_title = request.POST.get('blog_title','')
        blog_content = request.POST.get('blog_content','')
        tag_select = request.POST.getlist('tag_select')
        blog_author = request.user.expert_profile
        blog_datetime = datetime.datetime.now()
        tag_list = []

        # Collect Tag Instance Of Each Tag Id in tag_select into tag_list
        for tagId in tag_select:
            tag_item = Blog_Tag.objects.get(tag_id=int(tagId))
            tag_list.append(tag_item)

        print("Blog Author:", str(blog_author))
        print("Datetime:", str(blog_datetime))
        print("Blog Title:", str(blog_title))
        print("Blog Content:", str(blog_content))
        print("tag_list:", str(tag_list))

        new_blog = Blogpost(title=blog_title, content=blog_content, author=blog_author, datetime=blog_datetime)
        new_blog.save()

        # Save Each Blogpost <==> Tag Mapping in Blogpost_Tag Table
        for tagInstance in tag_list:
            blogpost_tag = Blogpost_Tag(blog_id=new_blog, tag_id=tagInstance)
            blogpost_tag.save()

        # Blog Write Success Message Page
        return render(request, 'accounts/blogWrittenSuccess.html')
    else:
        # Invalid Entry
        return render(request, 'accounts/blogWrittenSuccess.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_read(request, blog_identifier):
    # blog_identifier must be of the form articleName_blogId
    # articleName is blog_title with all non allowed characters replaced with '_'

    split_position = blog_identifier.rindex('_')
    articleName = blog_identifier[:split_position]
    blogId = blog_identifier[split_position+1:]
    print("blogId:",str(blogId))

    try:
        # Check If The Blog Exists In The Database
        target_blog = Blogpost.objects.get(blog_id=int(blogId))

        # Find Tags For This Blog
        tag_set = Blogpost_Tag.objects.filter(blog_id=target_blog)
        print("tag_set:", str(tag_set))
        
        # Display The Blog
        return render(request, 'accounts/blogTemplate.html', {'blog': target_blog, 'tag_set':tag_set})
    except:
        # If Blog Doesn't Exist Take To 404 Page
        return render(request, 'accounts/basic_layout.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_blog(request):
    blog=Blogpost.objects.all()

    # paginator logic
    colors = ['#6b5b95' , '#feb236' , '#d64161' , '#b5e7a0' , '#86af49' , '#92a8d1' , ' #034f84' , '#3e4444' ,
              '#80ced6' ,
              '#f7786b' , '#FF1493' , '#00FA9A' , '#008080' , '#FF6347' , '#8B0000' , '#FF8C00' , '#800080' ,
              '#00FF7F' ,
              '#2F4F4F']
    blogposts=[]

    paginator=Paginator(blog,8)
    page=request.GET.get('page')
    # posts=paginator.page(page)
    try:
        posts=paginator.get_page(page)


    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    for i in posts:
        c = random.choice ( colors )
        blogposts.append([i,c,i.title.replace(' ','_')])


    return render(request,'accounts/Blog.html',{'blogs':posts,'blogposts':blogposts})