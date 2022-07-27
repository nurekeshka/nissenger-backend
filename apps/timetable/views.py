from rest_framework import generics
from . import serializers
from . import models


class TeacherList(generics.ListAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
