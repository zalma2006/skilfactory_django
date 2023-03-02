from django.urls import path, include
from .views import NewsLists, BaseRegisterView, PostCreate, PostUpdate, PostDelete
from django.contrib.auth.views import LoginView, LogoutView
# Импортируем созданное нами представление

urlpatterns = [
    path('', (NewsLists.as_view()), name='post'),  # кэш для пробы
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('create/', PostCreate.as_view(), name='create'),
    path('<int:pk>/update', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    # path('<int:id>', cache_page(300)(NewsDetail.as_view()), name='new'),
    # path('', NewsLists.as_view(), name='news')
]