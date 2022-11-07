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
