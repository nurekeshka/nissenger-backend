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


class GroupsListSerializer(GroupSerializer):
    def to_representation(self, instance: models.Group):
        return {
            'name': instance.name,
            'classes': [{'grade': __class.grade, 'letter': __class.letter} for __class in instance.classes.all()]
        }


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ('id', 'name', 'timetable')


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('id', 'name', 'type', 'timetable')


class ClassroomSerializer(ModelSerializer):
    class Meta:
        model = models.Classroom
        fields = ('id', 'name', 'timetable')


class LessonSerializer(ModelSerializer):
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
                'starttime': instance.period.starttime,
                'endtime': instance.period.endtime,
            },
            'group': {
                'name': instance.group.name,
                'classes': [{'grade': __class.grade, 'letter': __class.letter} for __class in instance.group.classes.all()]
            }
        }


class PeriodSerializer(ModelSerializer):
    class Meta:
        model = models.Period
        fields = ('number', 'starttime', 'endtime', 'timetable')


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = models.School
        fields = ('id', 'name', 'city')
