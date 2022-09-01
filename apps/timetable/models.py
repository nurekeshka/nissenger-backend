from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from .exceptions import validate_class_letter
from django.db import models
from datetime import datetime
from datetime import time
from typing import Set


class Timetable(models.Model):
    download_date: datetime = models.DateTimeField(auto_now_add=True, verbose_name='download date')
    active: bool = models.BooleanField(default=False, verbose_name='active')

    class Meta:
        verbose_name = 'timetable'
        verbose_name_plural = 'timetables'
    
    def __str__(self):
        return str(self.download_date)
    
    def activate(self):
        for timetable in Timetable.objects.all():
            timetable.deactivate()
        
        self.active = True
        self.save()
    
    def deactivate(self):
        self.active = False
        self.save()


class Day(models.Model):
    name: str = models.CharField(verbose_name='name',
                            max_length=15, blank=False, null=False)

    class Meta:
        verbose_name = 'day'
        verbose_name_plural = 'days'

    def __str__(self):
        return self.name


class Class(models.Model):
    grade: int = models.IntegerField(verbose_name='grade', blank=False, 
        null=False, validators=[
            MaxValueValidator(limit_value=12),
            MinValueValidator(limit_value=7),
        ]
    )
    letter: str = models.CharField(verbose_name='letter', max_length=1, 
        blank=False, null=False, validators=[
            validate_class_letter
        ]
    )

    timetable: Timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'

    def __str__(self):
        return f'{self.grade}{self.letter}'


class Group(models.Model):
    name: str = models.CharField(max_length=255, verbose_name='name')
    classes: Set[Class] = models.ManyToManyField(Class, verbose_name='classes')
    timetable: Timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'
    
    def __str__(self):
        return f'{self.name}: {list(map(str, self.classes.all()))}'


class Teacher(models.Model):
    name: str = models.CharField(max_length=255, verbose_name='name')
    timetable: Timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        return self.name


class Subject(models.Model):
    name: str = models.CharField(max_length=255, verbose_name='name')
    timetable: Timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'
    
    def __str__(self):
        return self.name


class Office(models.Model):
    name: str = models.CharField(max_length=255, verbose_name='name')
    timetable: Timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'office'
        verbose_name_plural = 'offices'

    def __str__(self):
        return self.name


class Period(models.Model):
    number: int = models.IntegerField(verbose_name='number')
    start: time = models.TimeField(verbose_name='start')
    end: time = models.TimeField(verbose_name='end')

    timetable: Timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'period'
        verbose_name_plural = 'periods'
    
    def __str__(self):
        return ' - '.join((self.start.strftime('%H:%M'), self.end.strftime('%H:%M')))


class Lesson(models.Model):
    subject: Subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='subject')
    office: Office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name='office')
    teacher: Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='teacher')
    period: Period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name='period')
    group: Group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='group')
    day: Day = models.ForeignKey(Day, on_delete=models.CASCADE, verbose_name='day')

    timetable: Timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'
    
    def __str__(self):
        return self.subject.name
