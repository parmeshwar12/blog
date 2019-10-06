from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse 
from tinymce.models import HTMLField

# Create your models here.

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post',related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username 

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #comment_count = models.IntegerField(default = 0)
    #views_count = models.IntegerField(default = 0)
    content = HTMLField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:post', kwargs={
            'id': self.id
        })
    
    def get_created_url(self):
        return reverse('post:post', kwargs={
            'id': self.id
        })
    
    def get_update_url(self):
        return reverse('post:post-update', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('post:post-delete', kwargs={
            'id': self.id
        })

    @property
    def get_comments(self):
        return self.comments.order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def views_count(self):
        return PostView.objects.filter(post=self).count()

