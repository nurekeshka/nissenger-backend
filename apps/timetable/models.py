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
        return self.pk


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
