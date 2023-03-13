from rest_framework import serializers
from spr1.models import PerevalAdded, Users, Coords, Image


class UsersSerializer(serializers.BaseSerializer):
    class Meta:
        model = Users
        fields = ('email',
                  'fam',
                  'name',
                  'otc',
                  'phone')

    def to_internal_value(self, data):
        name = data.get('name')
        email = data.get('email')
        fam = data.get('fam')
        otc = data.get('otc')
        phone = data.get('phone')
        if not name:
            raise serializers.ValidationError({
                'name': 'name должно быть заполнено'})
        if not email:
            raise serializers.ValidationError({
                'email': 'email должно быть заполнено'})
        if not fam:
            raise serializers.ValidationError({
                'fam': 'fam должно быть заполнено'})
        if not otc:
            otc = ''
        if not phone:
            raise serializers.ValidationError({
                'phone': 'phone должно быть заполнено'})
        return {
            'name': name,
            'email': email,
            'fam': fam,
            'otc': otc,
            'phone': phone
        }

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'email': instance.email,
            'fam': instance.fam,
            'otc': instance.otc,
            'phone': instance.phone
        }

    def create(self, validated_data):
        return Users.objects.create(**validated_data)


class CoordsSerializer(serializers.BaseSerializer):
    class Meta:
        model = Users
        fields = ('latitude',
                  'longitude',
                  'height')

    def to_internal_value(self, data):
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        height = data.get('height')
        if not latitude:
            raise serializers.ValidationError({
                'latitude': 'широта должно быть заполнено'})
        elif not isinstance(latitude, float):
            raise serializers.ValidationError({
                'latitude': 'широта это число с плавающей точкой!'})
        else:
            latitude = float(latitude)
        if not longitude:
            raise serializers.ValidationError({
                'longitude': 'долгота должно быть заполнено'})
        elif not isinstance(longitude, float):
            raise serializers.ValidationError({
                'longitude': 'долгота это число с плавающей точкой!'})
        else:
            longitude = float(longitude)
        if not height:
            raise serializers.ValidationError({
                'height': 'Высота должно быть заполнено'})
        elif not isinstance(height, float):
            raise serializers.ValidationError({
                'height': 'Высота это число с плавающей точкой!'})
        else:
            height = float(height)
        return {'latitude': latitude,
                'longitude': longitude,
                'height': height}

    def to_representation(self, instance):
        return {'latitude': instance.latitude,
                'longitude': instance.longitude,
                'height': instance.height}

    def create(self, validated_data):
        return Coords.objects.create(**validated_data)


class ImagesSerializer(serializers.BaseSerializer):
    class Meta:
        model = Image
        fields = ('title',
                  'data')

    def to_internal_value(self, data):
        title = data.get('title')
        data = data.get('data')
        if not title:
            raise serializers.ValidationError({
                'title': 'Название картинки должно быть заполнено'})
        else:
            title = str(title)
        if not data:
            data = ''
            # raise serializers.ValidationError({
            #     'data': 'Картинка должна быть!'})
        return {'title': title,
                'data': data}

    def to_representation(self, instance):
        return {'title': instance.title,
                'data': instance.data}

    def create(self, validated_data):
        return Image.objects.create(**validated_data)


class PerevalAddedSerializer(serializers.ModelSerializer):
    users = UsersSerializer()
    coords = CoordsSerializer()
    images = ImagesSerializer()

    class Meta:
        model = PerevalAdded
        fields = ('title',
                  'other_titles',
                  'connect',
                  'users',
                  'coords',
                  'winter',
                  'summer',
                  'autumn',
                  'spring',
                  'images')
        # 'images_title',
        # 'images_data')
