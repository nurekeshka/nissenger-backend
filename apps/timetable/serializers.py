from rest_framework import serializers
from . import models


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Timetable
        fields = ('id', 'downloaded', 'school')


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('id', 'name')


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Class
        fields = ('id', 'grade', 'letter', 'timetable')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'name', 'classes', 'timetable')


class GroupsListSerializer(GroupSerializer):
    def to_representation(self, instance: models.Group):
        return {
            'name': instance.name,
            'classes': [{'grade': __class.grade, 'letter': __class.letter} for __class in instance.classes.all()]
        }


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('id', 'name', 'timetable')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('id', 'name', 'type', 'timetable')


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classroom
        fields = ('id', 'name', 'timetable')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ('id', 'subject', 'classroom', 'teacher',
                  'group', 'period', 'day', 'timetable')


class LessonsListSerializer(LessonSerializer):
    def to_representation(self, instance: models.Lesson):
        return {
            'subject': instance.subject.name,
            'classroom': instance.classroom.name,
            'teacher': instance.teacher.name,
            'day': instance.day.name,
            'period': {
                'number': instance.period.number,
                'start_time': instance.period.starttime,
                'end_time': instance.period.endtime,
            },
            'group': {
                'name': instance.group.name,
                'classes': [{'grade': __class.grade, 'letter': __class.letter} for __class in instance.group.classes.all()]
            }
        }


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Period
        fields = ('number', 'starttime', 'endtime', 'timetable')


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = ('id', 'name', 'city')
        depth = 1
