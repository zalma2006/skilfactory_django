from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from requests import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from . import serializers
from .models import PerevalAdded, Users
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_pereval(request):
    data = request.META

    # for image in data.get('images'):
    print(data)
    tmp_user = data.get('user')
    print(tmp_user)
    obj = PerevalAdded
    obj.beauty_title = data.get('beauty_title')
    obj.title = data.get('title')
    obj.other_titles = data.get('other_titles')
    obj.connect = data.get('connect')
    obj.user.name = data.get('user')['name']
    obj.user.email = data.get('user')['email']
    obj.user.fam = data.get('user')['fam']
    obj.user.otc = data.get('user')['otc']
    obj.user.phone = data.get('user')['phone']
    obj.coords.latitude = data.get('coords')['latitude']
    obj.coords.longitude = data.get('coords')['longitude']
    obj.coords.height = data.get('coords')['height']
    obj.winter = data.get('level')['winter']
    obj.summer = data.get('level')['summer']
    obj.autumn = data.get('level')['autumn']
    obj.spring = data.get('level')['spring']
    obj.status = 'new'
    obj.images.data = data.get('images')['data']
    obj.images.title = data.get('images')['title']
    obj.save()
    return HttpResponse(status=200)


class PerevalAddedListAPIView(CreateAPIView):
    serializer_class = serializers.PerevalAddedSerializer

    def get_queryset(self):
        return PerevalAdded.objects.all()



class UsersAddedListAPIView(CreateAPIView):
    serializer_class = serializers.UsersSerializer

    def get_queryset(self):
        return Users.objects.all()
