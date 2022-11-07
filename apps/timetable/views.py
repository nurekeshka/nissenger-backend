from rest_framework.response import Response
from rest_framework import generics
from rest_framework import views
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


class ClassroomList(generics.ListAPIView):
    queryset = models.Classroom.objects.filter(timetable__active=True)
    serializer_class = serializers.ClassroomSerializer


class TimetableLoadView(views.APIView):
    def post(self, request, *args, **kwargs):
        timetable = models.Timetable.objects.create()
