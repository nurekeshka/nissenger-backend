from rest_framework.test import APITestCase
from apps.timetable.models import *
from rest_framework import status
from django.urls import reverse


class ClassTestCase(APITestCase):
    def test_model_valid(self):
        for n in range(7, 13):
            Class.objects.create(grade=n, letter='A')
    
    def test_model_invalid(self):
        try:
            Class.objects.create(grade=1, letter='A')
            error = False
        except:
            error = True
        
        self.assertEqual(error, True)
