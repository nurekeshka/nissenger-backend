from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *


class ClassTestCase(APITestCase):
    def test_model_valid(self):
        pass
