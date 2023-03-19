from rest_framework import serializers
from spr1.models import PerevalAdded, Users, Coords, Image


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


class ImagesSerializer(serializers.ListField):

    def create(self, validated_data):
        images = [Image(**item) for item in validated_data]
        return Image.objects.bulk_create(images)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        list_serializer_class = ImagesSerializer()


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordSerializer()
    images = ImagesSerializer(child=ImageSerializer())

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
                  'images',
                  )

    def create(self, validated_data):
        users_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        image_data = validated_data.pop('images')
        user = Users.objects.create(**users_data)
        coords = Coords.objects.create(**coords_data)
        images = Image.objects.create(**image_data)
        pereval = PerevalAdded.objects.create(user=user, coords=coords, images=images, **validated_data)
        return pereval


