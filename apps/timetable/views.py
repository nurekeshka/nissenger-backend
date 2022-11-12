from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics
from rest_framework import views
from . import serializers
from . import models
import io


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


class SchoolList(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer


class RetrieveSchool(generics.RetrieveAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
