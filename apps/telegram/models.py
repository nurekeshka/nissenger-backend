from django.db import models


class Telegram(models.Model):
    id = models.IntegerField(
        primary_key=True, unique=True, null=False, blank=False, verbose_name='id')
    username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='username')
    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='first name')
    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='last name')

    class Meta:
        verbose_name = 'telegram'
        verbose_name_plural = 'telegrams'

    def get_full_name(self) -> str:
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.get_full_name()


# class Report(models.Model):
#     user = models.ForeignKey(
#         Telegram, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='user')
#     message = models.CharField(max_length=500, verbose_name='message')
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'report'
#         verbose_name_plural = 'reports'
