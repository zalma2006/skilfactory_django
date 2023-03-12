from django.urls import path, include
from .views import PerevalAddedListAPIView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from spr1.views import PerevalAddedListAPIView, create_pereval, UsersAddedListAPIView

schema_view = get_schema_view(
    openapi.Info(
        title='api_sprint1',
        default_version='v1',
        description='API',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('cr_pereval/', schema_view.as_view()),
    path('create_pereval/', create_pereval),
    path('perevaladded/', PerevalAddedListAPIView.as_view(), name='api_perevaladded'),
    path('usersadded/', UsersAddedListAPIView.as_view(), name='api_usersadded'),
]