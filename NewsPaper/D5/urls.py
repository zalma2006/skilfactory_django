from django.urls import path, include
# Импортируем созданное нами представление
from .views import (NewsLists, NewsDetail, NewsListsSearch, NewsCreate,
                    NewsUpdate, NewsDelete, BaseRegisterView, CategoryListView, subscribe, upgrade_me,
                    Index)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    # path('', cache_page(60)(NewsLists.as_view()), name='news'), # кэш для пробы
    # path('<int:id>', cache_page(300)(NewsDetail.as_view()), name='new'),
    path('', NewsLists.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='new'),
    path('search/', NewsListsSearch.as_view(), name='search'),
    path('create/', NewsCreate.as_view(), name='create'),
    path('<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('index/', Index.as_view(), name='index')
]
