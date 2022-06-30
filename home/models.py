from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=2000)
    image = models.ImageField(upload_to='category', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=1000)
    content = HTMLField()
    slug = models.SlugField(max_length=2000)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(upload_to='blog')
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_comment = models.TextField(max_length=5000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_comment[0:13]+'... by '+self.user.username

    def get_comments(self):
        return Comment.objects.filter(parent=self)


class Subscribe(models.Model):
    email = models.CharField(max_length=1000)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
