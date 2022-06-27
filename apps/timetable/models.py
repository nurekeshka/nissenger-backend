from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class Day(models.Model):
    name = models.CharField(verbose_name='name', max_length=15, blank=False, null=False)

    class Meta:
        verbose_name = 'day'
        verbose_name_plural = 'days'

    def __str__(self):
        return self.name


class Class(models.Model):
    grade = models.IntegerField(verbose_name='grade', blank=False, null=False, validators=[
            MaxValueValidator(limit_value=12),
            MinValueValidator(limit_value=7),
        ])
    letter = models.CharField(verbose_name='letter', max_length=1, blank=False, null=False)

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'
    
    def __str__(self):
        return f'{self.grade}{self.letter}'
