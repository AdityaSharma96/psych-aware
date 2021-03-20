from django.db import models
from accounts.models import Expert_Profile
# Create your models here.
class Blogpost(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=1000, default='')
    author = models.ForeignKey(to=Expert_Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        blogpost = str(self.blog_id) + " \n"
        blogpost = blogpost + " title = " + self.title + "\n"
        return blogpost

class Blog_Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50, default='')

    def __str__(self):
        blogtag = str(self.tag_id) + " \n"
        blogtag = blogtag + " tag = " + self.tag + "\n"
        return blogtag

class Blogpost_Tag(models.Model):
    blog_id = models.ForeignKey(to=Blogpost, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(to=Blog_Tag, on_delete=models.CASCADE)

    def __str__(self):
        blogpost = "blod_id = " + str(self.blog_id) + " \n"
        blogpost = blogpost + " tag_id = " + str(self.tag_id) + "\n"
        return blogpost
