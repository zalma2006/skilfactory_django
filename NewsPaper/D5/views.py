# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView,
                                  TemplateView)
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from .models import BaseRegisterForm, Category


class NewsLists(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dt_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 5


class NewsDetail(DetailView):
    model = Post

    template_name = 'new.html'

    context_object_name = 'new'

    pk_url_kwarg = 'id'


class NewsListsSearch(ListView):
    model = Post
    ordering = 'dt_create'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.group.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html',
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category_id=self.category).order_by('-dt_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objacts.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей!'

    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
