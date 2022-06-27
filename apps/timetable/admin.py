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
    fields = ('grade', 'letter')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'classes')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name', 'teachers')


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'timetable')
    fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'office', 'day', 'start', 'end', 'timetable')
    fields = ('subject', 'office', 'day', 'start', 'end')
