from rest_framework import generics
from . import serializers
from . import models


class TeacherList(generics.ListAPIView):
    queryset = models.Teacher.objects.filter(timetable__active=True)
    serializer_class = serializers.TeacherSerializer

class ClassList(generics.ListAPIView):
    queryset = models.Class.objects.filter(timetable__active=True)
    serializer_class = serializers.ClassSerializer


class PeriodList(generics.ListAPIView):
    queryset = models.Period.objects.filter(timetable__active=True)
    serializer_class = serializers.PeriodSerializer
