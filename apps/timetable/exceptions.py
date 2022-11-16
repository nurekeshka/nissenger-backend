from rest_framework.exceptions import APIException
from rest_framework import status


class SchoolNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'School not found in the database.'


class ClassNotFoundExceptions(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Class not found in the database.'
