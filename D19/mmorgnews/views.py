from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .models import Post, BaseRegisterForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import User
from .forms import PostForm
from django.core.cache import cache


class NewsLists(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'
    paginate_by = 10


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/post/'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')


class PostDetail(DetailView):
    template_name = 'post1.html'
    context_object_name = 'post1'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'new-{self.kwargs["pk"]}')
        print(obj)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'new-{self.kwargs["pk"]}', obj)
            print(obj)
        return obj


class Groups(ListView):
    model = Group
    template_name = 'upgrade.html'
    context_object_name = 'group'
