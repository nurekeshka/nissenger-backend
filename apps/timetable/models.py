from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='city')

    class Meta:
        verbose_name = 'school'
        verbose_name_plural = 'schools'

    def __str__(self):
        return self.name


class Timetable(models.Model):
    downloaded = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name='downloaded')
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, verbose_name='school')

    class Meta:
        verbose_name = 'timetable'
        verbose_name_plural = 'timetables'

    def __str__(self):
        return self.downloaded.strftime('%Y-%m-%d %H:%M:%S')


class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.CharField(max_length=25, verbose_name='name')

    class Meta:
        verbose_name = 'day'
        verbose_name_plural = 'days'

    def __str__(self):
        return self.name


class Period(models.Model):
    starttime = models.TimeField(verbose_name='start time')
    endtime = models.TimeField(verbose_name='end time')
    number = models.IntegerField(verbose_name='number')
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'period'
        verbose_name_plural = 'periods'

    def __str__(self):
        return ' - '.join((self.starttime.strftime('%H:%M'), self.endtime.strftime('%H:%M')))


class Classroom(models.Model):
    name = models.CharField(max_length=25, verbose_name='name')
    timetable = models.ForeignKey(
        Timetable, on_delete=models.CASCADE, verbose_name='timetable')

    class Meta:
        verbose_name = 'classroom'
        verbose_name_plural = 'classrooms'

    def __str__(self):
        return self.name
