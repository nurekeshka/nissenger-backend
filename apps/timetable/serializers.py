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


class GroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'name', 'classes', 'timetable')


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('id', 'name', 'timetable')


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('id', 'name', 'teachers', 'timetable')


class OfficeSerializer(ModelSerializer):
    class Meta:
        model = models.Office
        fields = ('id', 'name', 'timetable')


class LessonSerializer(ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ('id', 'subject', 'office', 'teacher',
                  'group', 'period', 'day', 'timetable')


class PeriodSerializer(ModelSerializer):
    class Meta:
        model = models.Period
        fields = ('number', 'start', 'end')
