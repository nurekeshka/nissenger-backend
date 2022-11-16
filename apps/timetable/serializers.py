from rest_framework.serializers import ModelSerializer
from . import models


class TimetableSerializer(ModelSerializer):
    class Meta:
        model = models.Timetable
        fields = ('id', 'downloaded', 'school')


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
        fields = ('id', 'name', 'timetable')


class ClassroomSerializer(ModelSerializer):
    class Meta:
        model = models.Classroom
        fields = ('id', 'name', 'timetable')


class LessonSerializer(ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ('id', 'subject', 'classroom', 'teacher',
                  'group', 'period', 'day', 'timetable')


class PeriodSerializer(ModelSerializer):
    class Meta:
        model = models.Period
        fields = ('number', 'starttime', 'endtime', 'timetable')


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = models.School
        fields = ('id', 'name', 'city')


def parse_lesson(lesson: dict):
    lesson['subject'] = models.Subject.objects.get(
        id=lesson['subject']).name
    lesson['classroom'] = models.Classroom.objects.get(
        id=lesson['classroom']).name
    lesson['teacher'] = models.Teacher.objects.get(
        id=lesson['teacher']).name
    lesson['period'] = PeriodSerializer(
        instance=models.Period.objects.get(id=lesson['period'])).data

    lesson['group'] = GroupSerializer(
        instance=models.Group.objects.get(id=lesson['group'])).data

    lesson['group']['classes'] = [ClassSerializer(
        instance=models.Class.objects.get(id=__class)).data for __class in lesson['group']['classes']]

    return lesson
