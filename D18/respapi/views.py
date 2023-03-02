import django_filters
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

from respapi.serializers import SchoolSerializer, SClassSerializer, StudentSerializer
from respapi.models import School, SClass, Student


class SchoolViewset(viewsets.ModelViewSet):
    queryset = School.objects.all().filter(is_active=True)
    serializer_class = SchoolSerializer

    def destroy(self, request, pk, format=None):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SClassViewset(viewsets.ModelViewSet):
    queryset = SClass.objects.all()
    serializer_class = SClassSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["grade", "school_id"]


class StudentViewest(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()
        school_id = self.request.query_params.get('school_id', None)
        sclass_id = self.request.query_params.get('class_id', None)
        if school_id is not None:
            queryset = queryset.filter(sclass__school_id=school_id)
        if sclass_id is not None:
            queryset = queryset.filter(sclass_id=sclass_id)
        return queryset
