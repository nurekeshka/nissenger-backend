from rest_framework.serializers import ModelSerializer
from . import models


class TimetableSerializer(ModelSerializer):
    class Meta:
        model = models.Timetable
        fields = ('id', 'download_date', 'publication_date')


class DaySerializer(ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('id', 'name')


class ClassSerializer(ModelSerializer):
    class Meta:
        model = models.Class
        fields = ('id', 'grade', 'letter', 'timetable')
