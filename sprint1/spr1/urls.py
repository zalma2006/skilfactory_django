from django.urls import path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from spr1.views import PerevalAddedListAPIView, get_pereval, pereval_update, EmailPerevalView

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
    path('perevaladded/', PerevalAddedListAPIView.as_view(), name='api_perevaladded'),
    path('perevaladded/<int:pk>', get_pereval),
    path('perevaladded/update/<int:pk>', pereval_update),
    path('perevaladded/user__email=<email>', EmailPerevalView.as_view())

]
