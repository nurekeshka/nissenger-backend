from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics
from rest_framework import status
from rest_framework import views

from apps.timetable import utils
from . import exceptions
from . import serializers
from . import models
import io


class SearchClass(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        json = JSONParser().parse(stream)

        try:
            timetable = models.Timetable.objects.get(
                school__name=json['school'], active=True)
        except models.Timetable.DoesNotExist:
            raise exceptions.TimetableNotFoundException()

        if models.Class.objects.filter(grade=json['grade'], letter=json['letter'], timetable=timetable).exists():
            return Response(status=status.HTTP_302_FOUND)
        else:
            raise exceptions.ClassNotFoundException()


class SchoolList(generics.ListAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer


class TimetableLoadView(views.APIView):
    def post(self, request: Request, *args, **kwargs):
        school = models.School.objects.get(pk=request.GET.get('school'))
        timetable = models.Timetable.objects.create(school=school)

        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        for lesson in data['timetable']:
            day = models.Day.objects.get_or_create(
                name=lesson['day']['name'])[0]
            teacher = models.Teacher.objects.get_or_create(
                timetable=timetable, name=lesson['teacher']['name'])[0]
            subject = models.Subject.objects.get_or_create(
                timetable=timetable, name=lesson['subject']['name'], type=lesson['subject']['type'])[0]
            classroom = models.Classroom.objects.get_or_create(
                timetable=timetable, name=lesson['classroom']['name'])[0]
            period = models.Period.objects.get_or_create(
                timetable=timetable, number=lesson['period']['number'],
                starttime=lesson['period']['starttime'],
                endtime=lesson['period']['endtime']
            )[0]

            classes = [models.Class.objects.get_or_create(grade=__class['grade'], letter=__class['letter'], timetable=timetable)[
                0] for __class in lesson['group']['classes']]

            exists = utils.search_for_group(
                lesson['group']['name'], classes).exists()

            if not exists:
                group = models.Group.objects.create(
                    timetable=timetable,
                    name=lesson['group']['name']
                )
                group.classes.set(classes)

            models.Lesson.objects.create(
                subject=subject, classroom=classroom,
                teacher=teacher, period=period, day=day,
                group=group, timetable=timetable,
            )

        return Response(status=status.HTTP_201_CREATED)


class TeachersList(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        json = JSONParser().parse(stream)

        try:
            timetable = models.Timetable.objects.get(
                school__name=json['school'], active=True)
        except models.Timetable.DoesNotExist:
            raise exceptions.TimetableNotFoundException()

        teachers = models.Teacher.objects.filter(timetable=timetable)
        serializer = serializers.TeacherSerializer(
            instance=teachers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LessonsList(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        try:
            timetable = models.Timetable.objects.get(
                school__name=data['school'], active=True)
        except models.Timetable.DoesNotExist:
            raise exceptions.TimetableNotFoundException()

        __class = models.Class.objects.get(
            timetable=timetable, grade=data['class']['grade'], letter=data['class']['letter'])

        lessons = models.Lesson.objects.filter(
            group__name=data['group'], group__classes__in=[__class], timetable=timetable)

        for profile in data['profile_groups']:
            lessons.union(models.Lesson.objects.filter(
                group__name=profile, group__classes__in=[__class], timetable=timetable))

        serializer = serializers.LessonsListSerializer(
            instance=lessons, many=True)
        return Response(data=serializer.data)


class ProfileSubjectsList(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        try:
            timetable = models.Timetable.objects.get(
                school__name=data['school'], active=True)
        except models.Timetable.DoesNotExist:
            raise exceptions.TimetableNotFoundException()

        subjects = models.Subject.objects.filter(
            timetable=timetable, type='PD')

        serializer = serializers.SubjectSerializer(
            instance=subjects, many=True)
        return Response(data=serializer.data)
