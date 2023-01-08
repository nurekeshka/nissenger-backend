from datetime import datetime

from rest_framework import generics, status, views
from rest_framework.request import Request
from rest_framework.response import Response

from . import constants, exceptions, models, serializers, utils


class SearchClass(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, json: dict, timetable, *args, **kwargs):
        try:
            try:
                __class = models.Class.objects.get(
                    grade=json['class']['grade'], letter=json['class']['letter'], timetable=timetable)
                serializer = serializers.ClassSerializer(instance=__class)
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            except models.Class.DoesNotExist:
                raise exceptions.ClassNotFoundException()
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler(
                'Class grade or letter was not provided.')


class SearchGroups(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, json: dict, timetable: models.Timetable, *args, **kwargs):
        try:
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
    @utils.json
    def post(self, request: Request, data: dict, *args, **kwargs):
        school = models.School.objects.get(pk=request.GET.get('school'))
        timetable = models.Timetable.objects.create(school=school)

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

        timetable.activate()
        timetable.report_to_parser()
        return Response(status=status.HTTP_201_CREATED)


class TeachersList(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, json: dict, timetable: models.Timetable, *args, **kwargs):
        teachers = models.Teacher.objects.filter(timetable=timetable)
        serializer = serializers.TeacherSerializer(
            instance=teachers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LessonsList(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, data: dict, timetable: models.Timetable, *args, **kwargs):
        try:
            __class = models.Class.objects.get(
                timetable=timetable, grade=data['class']['grade'], letter=data['class']['letter'])
        except models.Class.DoesNotExist:
            raise exceptions.ClassNotFoundException
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler(
                'Class grade or letter was not provided.')

        group = utils.search_for_group(
            data['group'], [__class], timetable).first()
        lessons = models.Lesson.objects.filter(group=group).exclude(
            subject__type=models.Subject.MESK_PREPARATION).exclude(
                subject__type=models.Subject.PROFILE_DIRECTED, subject__name='Математика').exclude(
                    subject__type=models.Subject.PROFILE_DIRECTED, subject__name='Математика (10)'
        )

        if data.get('profile_groups'):
            if __class.grade >= 11:
                if 'мат10' in data['profile_groups']:
                    lessons = lessons.union(models.Lesson.objects.filter(
                        group__classes__in=[__class], timetable=timetable,
                        subject__type=models.Subject.PROFILE_DIRECTED,
                        subject__name='Математика (10)',
                    ))

                    data['profile_groups'].remove('мат10')
                else:
                    math = models.Lesson.objects.filter(
                        group=group, timetable=timetable,
                        subject__type=models.Subject.PROFILE_DIRECTED,
                        subject__name='Математика',
                    )

                    lessons = lessons.union(math.all())

                for profile in data['profile_groups']:
                    try:
                        group = models.Group.objects.get(name=profile, classes__in=[
                            __class], timetable=timetable)
                    except models.Group.DoesNotExist:
                        # raise exceptions.GroupNotFoundExceptionHandler
                        continue

                    lessons = lessons.union(models.Lesson.objects.filter(
                        group__name=profile, group__classes__in=[__class], timetable=timetable))

            elif __class.grade == 10:
                try:
                    subject = models.Subject.objects.get(
                        name=data['profile_groups'][0], type=models.Subject.MESK_PREPARATION, timetable=timetable)
                except models.Subject.DoesNotExist:
                    raise exceptions.SubjectNotFoundExceptionHandler

                lessons = lessons.union(models.Lesson.objects.filter(
                    subject=subject, group=group, timetable=timetable
                ))

        if data.get('foreign_language'):
            for fl_group_name in data['foreign_language']:
                found_groups = models.Group.objects.filter(
                    name=fl_group_name, classes__in=[__class], timetable=timetable)

                for group in found_groups:
                    lessons = lessons.union(
                        models.Lesson.objects.filter(group=group))

        dictionary = {day.name: list() for day in models.Day.objects.all()}

        for lesson in lessons.all():
            dictionary[lesson.day.name].append(
                serializers.LessonsListSerializer(instance=lesson).data)

        response = [sorted(array, key=lambda x: x['period']['number'])
                    for array in dictionary.values()]
        return Response(data={'timetable': {'lessons': response}})


class ProfileSubjectsList(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, data: dict, timetable: models.Timetable, *args, **kwargs):
        subjects = models.Subject.objects.filter(
            timetable=timetable, type='PD')

        serializer = serializers.SubjectSerializer(
            instance=subjects, many=True)
        return Response(data=serializer.data)


class ProfileGroupsList(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, data: dict, timetable: models.Timetable, *args, **kwargs):
        subject = models.Subject.objects.get(
            name=data['subject'], type='PD', timetable=timetable)

        __class = models.Class.objects.get(
            grade=data['class']['grade'], letter=data['class']['letter'], timetable=timetable)

        unique_groups = set()

        for lesson in models.Lesson.objects.filter(subject=subject, timetable=timetable, group__classes__in=[__class]):
            unique_groups.add(lesson.group.pk)

        groups = [models.Group.objects.get(pk=id) for id in unique_groups]

        serializer = serializers.ProfileGroupsListSerializer(
            instance=groups, many=True)
        return Response(data=serializer.data)


class ForeignLanguageSubjects(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, data: dict, timetable: models.Timetable, *args, **kwargs):
        subjects = models.Subject.objects.filter(
            type='FL', timetable=timetable)

        serializer = serializers.SubjectSerializer(
            instance=subjects, many=True)
        return Response(data=serializer.data)


class LessonsListTeachers(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, data: dict, timetable: models.Timetable, *args, **kwargs):
        try:
            teacher = models.Teacher.objects.get(
                name=data['teacher'], timetable=timetable)
        except models.Teacher.DoesNotExist:
            raise exceptions.TeacherNotFoundExceptionHandler()

        lessons = models.Lesson.objects.filter(teacher=teacher)

        dictionary = {day.name: list() for day in models.Day.objects.all()}

        for lesson in lessons.all():
            dictionary[lesson.day.name].append(
                serializers.LessonsListSerializer(instance=lesson).data)

        response = [sorted(array, key=lambda x: x['period']['number'])
                    for array in dictionary.values()]
        return Response(data={'timetable': {'lessons': response}})


class MeskPreparationSubjects(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, json: dict, timetable: models.Timetable, *args, **kwargs):
        subjects = models.Subject.objects.filter(
            type=models.Subject.MESK_PREPARATION, timetable=timetable)
        serializer = serializers.SubjectSerializer(
            instance=subjects, many=True)

        return Response(serializer.data)


class Online(views.APIView):
    def get(self, request: Request, *args, **kwargs):
        return Response()


class EmptyClassroom(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, json: dict, timetable: models.Timetable, *args, **kwargs):
        now = datetime.now()
        try:
            day = models.Day.objects.get(name=constants.DAYS[now.weekday()])
        except models.Day.DoesNotExist:
            classrooms = models.Classroom.objects.filter(
                timetable=timetable).exclude(name='')
            serializer = serializers.ClassroomSerializer(
                instance=classrooms, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        periods = models.Period.objects.filter(
            timetable=timetable).order_by('number')

        time = now.time()
        current = time.hour * 60 + time.minute
        school_time = False

        for period in periods:
            if period.starttime.hour * 60 + period.starttime.minute > current:
                school_time = True
                break

        if not school_time:
            serializer = serializers.ClassroomSerializer(
                instance=models.Classroom.objects.filter(timetable=timetable), many=True)
            return Response(data=serializer.data)

        period = models.Period.objects.get(timetable=timetable, number=1)

        all_classrooms = set(map(lambda array: array[0], models.Classroom.objects.filter(
            timetable=timetable).exclude(name='').values_list('id')))
        busy_classrooms = set(map(lambda array: array[0], models.Lesson.objects.filter(
            period=period, day=day).exclude(name='').values_list('classroom')))

        empty_classrooms = [models.Classroom.objects.get(
            pk=id) for id in all_classrooms.difference(busy_classrooms)]

        serializer = serializers.ClassroomSerializer(
            instance=empty_classrooms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ClassroomLessons(views.APIView):
    @utils.json
    @utils.timetable
    def post(self, request: Request, json: dict, timetable: models.Timetable, *args, **kwargs):
        try:
            day_name = json.get(
                'day', constants.DAYS[datetime.now().weekday()])
            day = models.Day.objects.get(name=day_name)
        except models.Day.DoesNotExist:
            raise exceptions.DayNotFoundExceptionHandler()

        try:
            classroom = models.Classroom.objects.get(
                name=json['classroom'], timetable=timetable)
        except KeyError:
            raise exceptions.KeyErrorExceptionHandler(
                'Classroom was not provided.')
        except models.Classroom.DoesNotExist:
            raise exceptions.ClassNotFoundException()

        lessons = models.Lesson.objects.filter(
            day=day, classroom=classroom, timetable=timetable)

        serializer = serializers.LessonsListSerializer(
            instance=lessons, many=True)
        return Response(data=serializer.data)
