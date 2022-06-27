from rest_framework.test import APITestCase
from apps.timetable.exceptions import *
from apps.timetable.models import *
from rest_framework import status
from django.urls import reverse


class ClassTestCase(APITestCase):
    def test_model_valid(self):
        for n in range(7, 13):
            Class.objects.create(grade=n, letter='A').save()
    
    def test_model_invalid(self):
        with self.assertRaises(ValidationError):
            Class.objects.create(grade=1, letter='A').save()
