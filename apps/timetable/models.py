from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name
