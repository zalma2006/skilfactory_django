from rest_framework import serializers
from spr1.models import PerevalAdded, Users


class PerevalAddedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerevalAdded
        fields = ('title',
                  'other_titles',
                  'connect',
                  'user',
                  # 'user_email',
                  # 'user_fam',
                  # 'user_name',
                  # 'user_otc',
                  # 'user_phone',
                  # 'coords_latitude',
                  # 'coords_longitude',
                  # 'coords_height',
                  'coords',
                  'winter',
                  'summer',
                  'autumn',
                  'spring',
                  'images')
                  # 'images_title',
                  # 'images_data')

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('email',
                  'fam',
                  'name',
                  'otc',
                  'phone')