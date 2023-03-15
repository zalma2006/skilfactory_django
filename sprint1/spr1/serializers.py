import ast
import json

from rest_framework import serializers
from spr1.models import PerevalAdded, Users, Coords, Image


# class UsersSerializer(serializers.BaseSerializer):
#     class Meta:
#         model = Users
#         fields = ('email',
#                   'fam',
#                   'name',
#                   'otc',
#                   'phone')
#
#     def to_internal_value(self, data):
#         data = ast.literal_eval(data)
#         name = data.get('name')
#         email = data.get('email')
#         fam = data.get('fam')
#         otc = data.get('otc')
#         phone = data.get('phone')
#         if not name:
#             raise serializers.ValidationError({
#                 'name': 'name должно быть заполнено'})
#         if not email:
#             raise serializers.ValidationError({
#                 'email': 'email должно быть заполнено'})
#         if not fam:
#             raise serializers.ValidationError({
#                 'fam': 'fam должно быть заполнено'})
#         if not otc:
#             otc = ''
#         if not phone:
#             raise serializers.ValidationError({
#                 'phone': 'phone должно быть заполнено'})
#         return {
#             'name': name,
#             'email': email,
#             'fam': fam,
#             'otc': otc,
#             'phone': phone
#         }
#
#     def to_representation(self, instance):
#         return {
#             'name': instance.name,
#             'email': instance.email,
#             'fam': instance.fam,
#             'otc': instance.otc,
#             'phone': instance.phone
#         }
#
#     def create(self, validated_data):
#         return Users.objects.create(**validated_data)
#
#
# class CoordsSerializer(serializers.BaseSerializer):
#     class Meta:
#         model = Users
#         fields = ('latitude',
#                   'longitude',
#                   'height')
#
#     def to_internal_value(self, data):
#         data = ast.literal_eval(data)
#         latitude = data.get('latitude')
#         longitude = data.get('longitude')
#         height = data.get('height')
#
#         if not latitude:
#             raise serializers.ValidationError({
#                 'latitude': 'широта должно быть заполнено'})
#         else:
#             try:
#                 latitude = float(latitude)
#             except ValueError:
#                 raise serializers.ValidationError({
#                     'latitude': 'широта это число с плавающей точкой!'})
#         if not longitude:
#             raise serializers.ValidationError({
#                 'longitude': 'долгота должно быть заполнено'})
#         else:
#             try:
#                 longitude = float(longitude)
#             except ValueError:
#                 raise serializers.ValidationError({
#                     'longitude': 'долгота это число с плавающей точкой!'})
#         if not height:
#             raise serializers.ValidationError({
#                 'height': 'Высота должно быть заполнено'})
#         else:
#             try:
#                 height = float(height)
#             except ValueError:
#                 raise serializers.ValidationError({
#                     'height': 'Высота это число с плавающей точкой!'})
#         return {'latitude': latitude,
#                 'longitude': longitude,
#                 'height': height}
#
#     def to_representation(self, instance):
#         return {'latitude': instance.latitude,
#                 'longitude': instance.longitude,
#                 'height': instance.height}
#
#     def create(self, validated_data):
#         return Coords.objects.create(**validated_data)


# class ImagesSerializer(serializers.BaseSerializer):
#     class Meta:
#         model = Image
#         fields = ('title',
#                   'data')
#
#     def to_internal_value(self, data):
#         data = ast.literal_eval(data)
#         title = data.get('title')
#         data = data.get('data')
#         if not title:
#             raise serializers.ValidationError({
#                 'title': 'Название картинки должно быть заполнено'})
#         else:
#             title = str(title)
#         if not data:
#             data = ''
#             # raise serializers.ValidationError({
#             #     'data': 'Картинка должна быть!'})
#
#         return {'title': title,
#                 'data': data}
#
#     def to_representation(self, instance):
#         print(instance, type(instance))
#         return {'title': instance.title,
#                 'data': instance.data}
#
#     def create(self, validated_data):
#         return Image.objects.create(**validated_data)

# class ImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ('title',
#                   'data')
#         depth = 2

class UsersSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        images = [Users(**item) for item in validated_data]
        return Users.objects.bulk_create(images)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        list_serializer_class = UsersSerializer


class CoordsSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        images = [Coords(**item) for item in validated_data]
        return Coords.objects.bulk_create(images)


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'
        list_serializer_class = CoordsSerializer


class ImagesSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        images = [Image(**item) for item in validated_data]
        return Image.objects.bulk_create(images)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        list_serializer_class = ImagesSerializer


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordSerializer()
    images = ImageSerializer()

    class Meta:
        model = PerevalAdded
        fields = ('title',
                  'beauty_title',
                  'other_titles',
                  'connect',
                  'user',
                  'coords',
                  'winter',
                  'summer',
                  'autumn',
                  'spring',
                  'images')

    def create(self, validated_data):
        users_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        image_data = validated_data.pop('images')
        user = Users.objects.create(**users_data)
        coords = Coords.objects.create(**coords_data)
        images = Image.objects.create(**image_data)
        pereval = PerevalAdded.objects.create(user=user, coords=coords, images=images, **validated_data)
        return pereval


