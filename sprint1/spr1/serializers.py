from rest_framework import serializers, request
from spr1.models import PerevalAdded, Users, Coords, Image, PerevalImage


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
    per = ImagesSerializer(child=ImageSerializer())

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
                  'per',
                  )

    def create(self, validated_data):
        users_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        image_data = validated_data.pop('per')
        user = Users.objects.create(**users_data)
        coords = Coords.objects.create(**coords_data)
        pereval = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)
        for img in image_data:
            image = Image.objects.create(**img)
            PerevalImage.objects.create(image=image, pereval=pereval)
        return pereval

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.content)
        instance.beauty_title = validated_data.get('beauty_title', instance.content)
        instance.other_titles = validated_data.get('other_titles', instance.content)
        instance.connect = validated_data.get('connect', instance.content)
        instance.coords = validated_data.get('coords', instance.created)
        instance.winter = validated_data.get('winter', instance.created)
        instance.summer = validated_data.get('summer', instance.created)
        instance.autumn = validated_data.get('autumn', instance.created)
        instance.spring = validated_data.get('spring', instance.created)
        instance.images = validated_data.get('images', instance.created)
        instance.save()
        return instance


class PerevalFindElement(serializers.ModelSerializer):
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
                  'status',
                  )
