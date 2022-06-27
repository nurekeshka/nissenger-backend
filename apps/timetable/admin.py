from django.contrib import admin
from .models import *


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'download_date', 'publication_date')
    fields = ('publication_date',)


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ('name',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('grade', 'letter', 'timetable')
    fields = ('grade', 'letter', 'timetable')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'classes', 'timetable')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'timetable')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'teachers', 'timetable')


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'timetable')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'office', 'teacher', 'group', 'day', 'start', 'end', 'timetable')
    fields = ('subject', 'office', 'teacher', 'group', 'day', 'start', 'end', 'timetable')
