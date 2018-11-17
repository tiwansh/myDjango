from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from django import forms
from django.conf import settings

# Create your models here.
from tinymce import HTMLField


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    text = HTMLField('Content')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    post_image = models.FileField(blank=True)
    draft = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/post/%i" % self.id


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved = models.BooleanField(default=True)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=100, blank=True)
    location = models.TextField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.FileField(default='default_pic.png')

    def __str__(self):
        return self.bio

    def publish(self):
        self.save()

    def get_absolute_url(self):
        return "/profile/%i" % self.id
