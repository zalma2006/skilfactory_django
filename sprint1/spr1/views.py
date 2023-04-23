import os
import re
from collections import OrderedDict
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ViewSet

from . import serializers
from .models import PerevalAdded, PerevalImages, Image, Users, Coords
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()


class PerevalAddedListAPIView(CreateAPIView):
    serializer_class = serializers.PerevalAddedSerializer

    def get_queryset(self):
        return PerevalAdded.objects.all()


def get_pereval(_, pk):
    resp = PerevalAdded.objects.filter(pk=pk).values()
    images = PerevalImages.objects.filter(pereval=pk).values()
    imgs = []
    for img in images:
        image = Image.objects.filter(pk=img['image_id'])
        imgs.append(image.values()[0])
    resp_dict = resp[0]
    resp_dict['images'] = imgs
    print(resp_dict)
    return JsonResponse(resp_dict)


class EmailPerevalView(ListAPIView):
    serializer_class = serializers.PerevalAddedSerializer

    def get_queryset(self):
        return PerevalAdded.objects.all()

    def filter_queryset(self, queryset):
        request = self.request
        email = request.parser_context['kwargs']['email']
        queryset = PerevalAdded.objects.filter(user__email=email)
        return queryset


def update_dict(query):
    user_data = {}
    coords_data = {}
    us_coord = False
    query = dict(query)
    tmp_query = dict()
    images_data = []
    for k, v in query.items():
        tmp_v = v[0]
        tmp_k = k
        if isinstance(tmp_k, str) and tmp_k.__contains__('.'):
            us_coord = True
            tmp_k1 = tmp_k.split('.')
            if 'coords' in tmp_k1:
                tmp_v = float(tmp_v)
                coords_data[tmp_k1[-1]] = tmp_v
            elif 'user' in tmp_k1:
                user_data[tmp_k1[-1]] = tmp_v
        if isinstance(tmp_k, str) and tmp_k.startswith('images'):
            idx = int(re.findall('\d', tmp_k)[0])
            tmp_k1 = str(tmp_k).split(']')[-1]
            tmp_k = str(tmp_k).split('[')[0]
            tmp_v = (idx, tmp_k1, tmp_v)
            images_data.append(tmp_v)
        if not str(tmp_k).startswith('images'):
            if not str(tmp_k).__contains__('.'):
                tmp_query[tmp_k] = tmp_v
    if us_coord:
        tmp_query['user'] = user_data
        tmp_query['coords'] = coords_data
    tmp_query['images'] = images_data
    return tmp_query


@csrf_exempt
def pereval_update(request, pk):
    data = request.POST
    files = request.FILES
    data = update_dict(data)
    files = update_dict(files)

    def ordered_dict_image(tmp_data: list, tmp_files: list):
        # объединяем поля из файлов и текстовых полей
        vals = []
        for tmp1 in tmp_data:
            for tmp2 in tmp_files:
                if tmp1[0] == tmp2[0]:
                    ord_dict = OrderedDict([(tmp1[1], tmp1[2]), (tmp2[1], tmp2[2])])
                    vals.append(ord_dict)
        return vals

    def update_pereval(data1, pereval1):
        if pereval1.title != data1['title']:
            pereval1.title = data1['title']
        if pereval1.beauty_title != data1['beauty_title']:
            pereval1.beauty_title = data1['beauty_title']
        if pereval1.other_titles != data1['other_titles']:
            pereval1.other_titles = data1['other_titles']
        if pereval1.connect != data1['connect']:
            if isinstance(data1['connect'], str) and len(data1['connect']) == 1:
                pereval1.connect = data1['connect']
        if pereval1.winter != data1['winter']:
            pereval1.winter = data1['winter']
        if pereval1.summer != data1['summer']:
            pereval1.summer = data1['summer']
        if pereval1.autumn != data1['autumn']:
            pereval1.autumn = data1['autumn']
        if pereval1.spring != data1['spring']:
            pereval1.spring = data1['spring']
        if pereval1.status != data1['status']:
            pereval1.status = data1['status']
        return pereval1

    def update_images(images_send1, images_data1, pereval1):
        # обновляем данные в таблицах Image и таблице связи ImagePereval
        # возможно количество фоток будет больше при обновлении поэтому необходимо досоздать записи в таблицах Image и
        # таблице связей PerevalImages
        if len(images_send1) == len(images_data1):
            for idx1, img_send in enumerate(images_send1):
                image = Image.objects.get(pk=img_send['image_id'])
                image.title = images_data[idx1]['title']
                image.data = images_data[idx1]['data']
                image.save()
        elif len(images_send1) < len(images_data):
            for idx1 in range(1, len(images_data) + 1, 1):
                image_id = None
                if idx1 <= len(images_send1):
                    image_id = images_send1[idx1 - 1]['image_id']
                try:
                    image = Image.objects.get(pk=image_id)
                    image.title = images_data[idx1]['title']
                    image.data = images_data[idx1]['data']
                    image.save()
                except ObjectDoesNotExist:
                    image = Image.objects.create(**images_data1[idx1 - 1])
                    PerevalImages.objects.create(pereval=pereval1, image=image)

    data['images'] = ordered_dict_image(data['images'], files['images'])
    del files
    pereval, images = None, None
    try:
        pereval = PerevalAdded.objects.get(pk=pk)
        images_send = PerevalImages.objects.filter(pereval=pk).values()
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'такого ключа не существует'})
    if pereval and images_send:
        if pereval.status != 'new':
            return JsonResponse({'state': '0', 'message': f'status = {pereval.status}, обновить данные уже нельзя'})
        else:
            images_data = data.pop('images')
            data.pop('user')
            # update coords
            coords_data = data.pop('coords')
            coords = Coords.objects.get(pk=pereval.coords_id)
            if coords.latitude != coords_data['latitude']:
                coords.latitude = coords_data['latitude']
            if coords.longitude != coords_data['longitude']:
                coords.longitude = coords_data['longitude']
            if coords.height != coords_data['height']:
                coords.height = coords_data['height']
            coords.save()
            if len(images_send) <= len(images_data):
                update_images(images_send, images_data, pereval)
            else:
                for idx in range(len(images_send), (len(images_send) - len(images_data)) - 1, -1):
                    # сначала удаляем лишние картинки из БД, потом обновляем данные
                    image = Image.objects.get(pk=images_send[idx - 1]['image_id'])
                    path_file = f"{str(os.getenv('FILE_DIR'))}{image.data.url}"
                    if os.path.isfile(path_file):
                        os.remove(path_file)
                    Image.objects.get(pk=images_send[idx - 1]['image_id']).delete()
                images_send = PerevalImages.objects.filter(pereval=pk).values()
                update_images(images_send, images_data, pereval)
            pereval = update_pereval(data, pereval)
            pereval.save()
            return JsonResponse({'state': '1'})

    # if request.method == 'GET':
    #     try:
    #         pereval = PerevalAdded.objects.get(pk=pk)
    #         pereval_serializer = serializers.PerevalFindElement(pereval)
    #         return JsonResponse(pereval_serializer.data)
    #     except PerevalAdded.DoesNotExist:
    #         return JsonResponse({'message': 'Такой записи не существует'})

# @api_view(['PATCH'])
# def perevalupdate(request, pk):
#     if request.method == 'PATCH':
#         try:
#             new_data = JSONParser().parse(request)
#             if new_data.get('status', None) == 'new':
#                 pereval = PerevalAdded.objects.get(pk=pk)
#                 pereval.beauty_title = new_data.get('beauty_title', None)
#                 pereval.other_titles = new_data.get('other_titles', None)
#                 pereval.connect = new_data.get('connect', None)
#                 pereval.coords = new_data.get('coords', None)
#                 pereval.winter = new_data.get('winter', None)
#                 pereval.summer = new_data.get('summer', None)
#                 pereval.autumn = new_data.get('autumn', None)
#                 pereval.spring = new_data.get('spring', None)
#                 pereval.images = new_data.get('images', None)
#                 pereval_serializer = serializers.PerevalAddedSerializer(pereval)
#                 if pereval_serializer.is_valid():
#                     pereval_serializer.save()
#                     return JsonResponse({'state': '1'})
#             else:
#                 return JsonResponse({'message': f'элемент имеет статус {new_data.get("status", None)}, '
#                                                 f'элемент не может быть изменён'})
#         except PerevalAdded.DoesNotExist:
#             return JsonResponse({'state': '0', 'error': 'элемент не найден'})
