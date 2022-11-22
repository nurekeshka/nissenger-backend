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
            try:
                city = models.City.objects.get(name=json['school']['city'])
            except models.City.DoesNotExist:
                raise exceptions.CityNotFoundExceptionHandler()

            try:
                school = models.School.objects.get(
                    name=json['school']['name'], city=city)
            except models.School.DoesNotExist:
                raise exceptions.SchoolNotFoundExceptionHandler()

            try:
                timetable = models.Timetable.objects.get(
                    school=school, active=True)
            except models.Timetable.DoesNotExist:
                raise exceptions.TimetableNotFoundException()

            try:
                __class = models.Class.objects.get(
                    grade=json['class']['grade'], letter=json['class']['letter'], timetable=timetable)
                serializer = serializers.ClassSerializer(instance=__class)
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            except models.Class.DoesNotExist:
                raise exceptions.ClassNotFoundException()
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler()


class SearchGroups(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        json = JSONParser().parse(stream)

        try:
            try:
                city = models.City.objects.get(name=json['school']['city'])
            except models.City.DoesNotExist:
                raise exceptions.CityNotFoundExceptionHandler()

            try:
                school = models.School.objects.get(
                    name=json['school']['name'], city=city)
            except models.School.DoesNotExist:
                raise exceptions.SchoolNotFoundExceptionHandler()

            try:
                timetable = models.Timetable.objects.get(
                    school=school, active=True)
            except models.Timetable.DoesNotExist:
                raise exceptions.TimetableNotFoundException()

            try:
                classes = [models.Class.objects.get(
                    grade=__class['grade'], letter=__class['letter'], timetable=timetable) for __class in json['group']['classes']]
            except models.Class.DoesNotExist:
                raise exceptions.ClassNotFoundException()

            group = utils.search_for_group(
                name=json['group']['name'], classes=classes, timetable=timetable)

            if not group.exists():
                raise exceptions.GroupNotFoundExceptionHandler()

            serializer = serializers.GroupsListSerializer(
                instance=group, many=True)

            return Response(data=serializer.data)
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler()


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
                lesson['group']['name'], classes, timetable).exists()

            if exists:
                group = utils.search_for_group(
                    lesson['group']['name'], classes, timetable).first()
            else:
                group = models.Group.objects.create(
                    timetable=timetable,
                    name=lesson['group']['name']
                )
                group.classes.set(classes)
                group.save()

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
            try:
                city = models.City.objects.get(name=json['school']['city'])
            except models.City.DoesNotExist:
                raise exceptions.CityNotFoundExceptionHandler()

            try:
                school = models.School.objects.get(
                    name=json['school']['name'], city=city)
            except models.School.DoesNotExist:
                raise exceptions.SchoolNotFoundExceptionHandler()

            try:
                timetable = models.Timetable.objects.get(
                    school=school, active=True)
            except models.Timetable.DoesNotExist:
                raise exceptions.TimetableNotFoundException()
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler()

        teachers = models.Teacher.objects.filter(timetable=timetable)
        serializer = serializers.TeacherSerializer(
            instance=teachers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LessonsList(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        try:
            city = models.City.objects.get(name=data['school']['city'])
        except models.City.DoesNotExist:
            raise exceptions.CityNotFoundExceptionHandler()

        try:
            school = models.School.objects.get(
                name=data['school']['name'], city=city)
        except models.School.DoesNotExist:
            raise exceptions.SchoolNotFoundExceptionHandler()

        try:
            timetable = models.Timetable.objects.get(
                school=school, active=True)
        except models.Timetable.DoesNotExist:
            raise exceptions.TimetableNotFoundException()

        try:
            __class = models.Class.objects.get(
                timetable=timetable, grade=data['class']['grade'], letter=data['class']['letter'])
        except models.Class.DoesNotExist:
            raise exceptions.ClassNotFoundException
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler(
                'Class grade or letter was not provided')

        group = utils.search_for_group(
            data['group'], [__class], timetable).first()
        lessons = models.Lesson.objects.filter(group=group)

        if data.get('profile_groups'):
            for profile in data['profile_groups']:
                lessons = lessons.union(models.Lesson.objects.filter(
                    group__name=profile, group__classes__in=[__class], timetable=timetable))

        if data.get('foreign_language'):
            foreign_language_groups = models.Group.objects.filter(
                name=data['foreign_language'], classes__in=[__class], timetable=timetable)

            for group in foreign_language_groups:
                lessons = lessons.union(
                    models.Lesson.objects.filter(group=group))

        serializer = serializers.LessonsListSerializer(
            instance=utils.sort_lessons_by_day_and_period(lessons), many=True)
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


class ProfileGroupsList(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        try:
            timetable = models.Timetable.objects.get(
                school__name=data['school'], active=True)
        except models.Timetable.DoesNotExist:
            raise exceptions.TimetableNotFoundException()

        subject = models.Subject.objects.get(
            name=data['subject'], type='PD', timetable=timetable)

        __class = models.Class.objects.get(
            grade=data['grade'], letter=data['letter'], timetable=timetable)

        lessons = models.Lesson.objects.distinct('group').filter(
            subject=subject, timetable=timetable,
            group__classes__in=[__class])

        groups = [lesson.group for lesson in lessons.all()]

        serializer = serializers.GroupsListSerializer(
            instance=groups, many=True)
        return Response(data=serializer.data)


class ForeignLanguageSubjects(views.APIView):
    def get(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        try:
            timetable = models.Timetable.objects.get(
                school__name=data['school'], active=True)
        except models.Timetable.DoesNotExist:
            raise exceptions.TimetableNotFoundException()

        subjects = models.Subject.objects.filter(
            type='FL', timetable=timetable)

        serializer = serializers.SubjectSerializer(
            instance=subjects, many=True)
        return Response(data=serializer.data)
