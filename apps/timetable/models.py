from datetime import datetime, time
from typing import Set
from django.db import models


class City(models.Model):
    name: str = models.CharField(max_length=50, verbose_name='name')

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class School(models.Model):
    name: str = models.CharField(max_length=50, verbose_name='name')
    city: City = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='city')

    class Meta:
        verbose_name = 'school'
        verbose_name_plural = 'schools'

    def __str__(self):
        return f'{self.name} - {str(self.city)}'


class Timetable(models.Model):
    downloaded: datetime = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name='downloaded')
    school: School = models.ForeignKey(
        School, on_delete=models.CASCADE, verbose_name='school')
    active: bool = models.BooleanField(default=False, verbose_name='active')

    class Meta:
        verbose_name = 'timetable'
        verbose_name_plural = 'timetables'

    def __str__(self):
        return self.downloaded.strftime('%Y-%m-%d %H:%M:%S')

    def activate(self):
        for timetable in Timetable.objects.filter(school=self.school):
            timetable.active = False

        self.active = True
        self.save()


class Subject(models.Model):
    name: str = models.CharField(max_length=50, verbose_name='name')
    timetable: Timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name: str = models.CharField(max_length=50, verbose_name='name')
    timetable: Timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        return self.name


class Day(models.Model):
    name: str = models.CharField(max_length=25, verbose_name='name')

    class Meta:
        verbose_name = 'day'
        verbose_name_plural = 'days'

    def __str__(self):
        return self.name


class Period(models.Model):
    starttime: time = models.TimeField(verbose_name='start time')
    endtime: time = models.TimeField(verbose_name='end time')
    number: int = models.IntegerField(verbose_name='number')
    timetable: Timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'period'
        verbose_name_plural = 'periods'

    def __str__(self):
        return ' - '.join((self.starttime.strftime('%H:%M'), self.endtime.strftime('%H:%M')))


class Classroom(models.Model):
    name: str = models.CharField(max_length=25, verbose_name='name')
    timetable: Timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'classroom'
        verbose_name_plural = 'classrooms'

    def __str__(self):
        return self.name


class Class(models.Model):
    grade: int = models.IntegerField(verbose_name='grade')
    letter: str = models.CharField(max_length=1, verbose_name='letter')
    timetable: Timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'

    def __str__(self):
        return f'{self.grade}{self.letter}'


class Group(models.Model):
    name: str = models.CharField(max_length=25, verbose_name='name')
    classes: Set[Class] = models.ManyToManyField(Class, verbose_name='classes')
    timetable: Timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    subject: Subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name='subject')
    classroom: Classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, verbose_name='classroom')
    teacher: Teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name='teacher')
    period: Period = models.ForeignKey(
        Period, on_delete=models.CASCADE, verbose_name='period')
    group: Group = models.ForeignKey(
        Group, on_delete=models.CASCADE, verbose_name='group')
    day: Day = models.ForeignKey(
        Day, on_delete=models.CASCADE, verbose_name='day')

    timetable: Timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'

    def __str__(self):
        return self.subject.name
