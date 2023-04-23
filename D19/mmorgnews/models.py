from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from markdownx.models import MarkdownxField
from django.contrib.auth.models import Group, User
from annoying.fields import AutoOneToOneField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings


# Create your models here.
class Users(models.Model):
    user = models.CharField(unique=True, max_length=150)
    name = models.CharField(max_length=50, unique=False, null=False)
    email = models.EmailField()

    def __str__(self):
        return f'user: {self.name} email: {self.email}'


class Author(models.Model):
    author = models.CharField(unique=True, default='', max_length=150)

    def __str__(self):
        return f'{self.author}'


class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=255)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.category_name


class Post(models.Model):
    category = models.ManyToManyField(Category, through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = MarkdownxField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse(f'post')


class Comment(models.Model):
    text = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(f'post')


class News(models.Model):
    category = models.ManyToManyField(Category, through='NewsCategory')
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)

    def save(self, commit=True):
        user = super().save()
        users = Users(user=user.username, email=user.email, name=user.get_full_name())
        users.save()
        author = Author(author=user.username)
        author.save()
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user
