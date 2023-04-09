
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from . import serializers
from .models import PerevalAdded

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view


class PerevalAddedListAPIView(CreateAPIView):
    serializer_class = serializers.PerevalAddedSerializer

    def get_queryset(self):
        return PerevalAdded.objects.all()


class PerevalFind(RetrieveAPIView):
    serializer_class = serializers.PerevalFindElement

    def get_queryset(self):
        return PerevalAdded.objects.all()







    # if request.method == 'GET':
    #     try:
    #         pereval = PerevalAdded.objects.get(pk=pk)
    #         pereval_serializer = serializers.PerevalFindElement(pereval)
    #         return JsonResponse(pereval_serializer.data)
    #     except PerevalAdded.DoesNotExist:
    #         return JsonResponse({'message': 'Такой записи не существует'})


@api_view(['PATCH'])
def perevalupdate(request, pk):
    if request.method == 'PATCH':
        try:
            new_data = JSONParser().parse(request)
            if new_data.get('status', None) == 'new':
                pereval = PerevalAdded.objects.get(pk=pk)
                pereval.beauty_title = new_data.get('beauty_title', None)
                pereval.other_titles = new_data.get('other_titles', None)
                pereval.connect = new_data.get('connect', None)
                pereval.coords = new_data.get('coords', None)
                pereval.winter = new_data.get('winter', None)
                pereval.summer = new_data.get('summer', None)
                pereval.autumn = new_data.get('autumn', None)
                pereval.spring = new_data.get('spring', None)
                pereval.images = new_data.get('images', None)
                pereval_serializer = serializers.PerevalAddedSerializer(pereval)
                if pereval_serializer.is_valid():
                    pereval_serializer.save()
                    return JsonResponse({'state': '1'})
            else:
                return JsonResponse({'message': f'элемент имеет статус {new_data.get("status", None)}, '
                                                f'элемент не может быть изменён'})
        except PerevalAdded.DoesNotExist:
            return JsonResponse({'state': '0', 'error': 'элемент не найден'})
