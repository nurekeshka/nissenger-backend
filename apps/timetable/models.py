from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from .exceptions import validate_class_letter
from django.db import models


class Timetable(models.Model):
    download_date = models.DateTimeField(auto_now_add=True, verbose_name='download date')
    publication_date = models.DateTimeField(default='', blank=True, verbose_name='publication date')

    class Meta:
        verbose_name = 'timetable'
        verbose_name_plural = 'timetables'
    
    def __str__(self):
        return str(self.publication_date)


class Day(models.Model):
    name = models.CharField(verbose_name='name',
                            max_length=15, blank=False, null=False)

    class Meta:
        verbose_name = 'day'
        verbose_name_plural = 'days'

    def __str__(self):
        return self.name


class Class(models.Model):
    grade = models.IntegerField(verbose_name='grade', blank=False, 
        null=False, validators=[
            MaxValueValidator(limit_value=12),
            MinValueValidator(limit_value=7),
        ]
    )
    letter = models.CharField(verbose_name='letter', max_length=1, 
        blank=False, null=False, validators=[
            validate_class_letter
        ]
    )

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'

    def __str__(self):
        return f'{self.grade}{self.letter}'


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    classes = models.ManyToManyField(Class, verbose_name='classes')
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'
    
    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    teachers = models.ManyToManyField(Teacher, verbose_name='teachers')
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'
    
    def __str__(self):
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'office'
        verbose_name_plural = 'offices'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='subject')
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name='office')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='teacher')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='group')

    start = models.TimeField(verbose_name='start')
    end = models.TimeField(verbose_name='end')
    day = models.ForeignKey(Day, on_delete=models.CASCADE, verbose_name='day')

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'
    
    def __str__(self):
        return self.subject.name
