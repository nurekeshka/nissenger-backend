from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from apps.timetable.models import *
from rest_framework import status
from django.urls import reverse


class ClassTestCase(APITestCase):
    def test_model_valid(self):
        for n in range(7, 13):
            Class.objects.create(grade=n, letter='A').full_clean()
    
    def test_model_invalid(self):
        with self.assertRaises(ValidationError):
            Class.objects.create(grade=1, letter='A').full_clean()
        with self.assertRaises(ValidationError):
            Class.objects.create(grade=11, letter='1').full_clean()
