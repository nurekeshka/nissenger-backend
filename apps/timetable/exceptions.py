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


class SchoolNotFoundExceptionHandler(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'School not found in the database.'


class GroupNotFoundExceptionHandler(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Group not found in the database.'


class ProfileGroupNotFoundExceptionHandler(APIException):
    status_code = status.HTTP_410_GONE
    default_detail = 'Profile group not found in the database.'


class TeacherNotFoundExceptionHandler(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Teacher not found in the database.'


class SubjectNotFoundExceptionHandler(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Subject not found in the database.'
