from django.urls import path, include

urlpatterns = [
    path("msg/", include("spr1.urls"))
]