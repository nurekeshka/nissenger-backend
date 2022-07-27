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
    list_filter = ('timetable__id',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'classes', 'timetable')
    list_filter = ('timetable__id',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'timetable')
    search_fields = ('id', 'name')
    list_filter = ('timetable__id',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'timetable')
    list_filter = ('timetable__id',)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'timetable')
    list_filter = ('timetable__id',)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('number', 'start', 'end', 'timetable')
    fields = ('number', 'start', 'end', 'timetable')
    list_filter = ('timetable__id',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'office', 'teacher', 'group', 'day', 'period', 'timetable')
    fields = ('subject', 'office', 'teacher', 'group', 'day', 'period', 'timetable')
    search_fields = ('subject', 'office', 'teacher', 'group', 'day', 'period')
    list_filter = ('timetable__id',)
