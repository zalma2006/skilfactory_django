from rest_framework.generics import CreateAPIView
from . import serializers
from .models import PerevalAdded


class PerevalAddedListAPIView(CreateAPIView):
    serializer_class = serializers.PerevalAddedSerializer

    def get_queryset(self):
        return PerevalAdded.objects.all()
