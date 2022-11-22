from rest_framework.exceptions import APIException
from rest_framework import status


class TimetableNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Active version of timetable for this school not found in the database.'


class ClassNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Class not found in the database.'


class KeyErrorExceptionHandler(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Some arguments were not provided.'


class CityNotFoundExceptionHandler(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'City not found in the database.'
