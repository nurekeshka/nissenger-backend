from django.db import models


class Version(models.Model):
    major = models.PositiveSmallIntegerField(verbose_name='major')
    minor = models.PositiveSmallIntegerField(verbose_name='minor')
    patch = models.PositiveSmallIntegerField(verbose_name='patch')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'version'
        verbose_name_plural = 'versions'

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'
