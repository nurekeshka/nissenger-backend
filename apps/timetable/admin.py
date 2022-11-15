from django.contrib import messages
from django.contrib import admin
from .models import *


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ('name',)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    fields = ('name', 'city')


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'downloaded', 'active', 'school')
    readonly_fields = ['active']
    actions = ('activate',)

    @admin.action(description='Опубликовать')
    def activate(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(
                request, 'Можно опубликовать только одну версию расписания', level=messages.ERROR)
        else:
            timetable = queryset[0]
            timetable.activate()
            self.message_user(
                request, 'Расписание успешно опубликовано', level=messages.SUCCESS)


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ('name',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade', 'letter', 'timetable')
    fields = ('grade', 'letter', 'timetable')
    list_filter = ('timetable__id',)
    search_fields = ('grade', 'letter')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'timetable')
    fields = ('name', 'classes', 'timetable')
    list_filter = ('timetable__id',)
    search_fields = ('id', 'name', 'classes__id')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'timetable')
    fields = ('name', 'timetable')
    search_fields = ('id', 'name')
    list_filter = ('timetable__id',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'timetable')
    fields = ('name', 'timetable')
    list_filter = ('timetable__id',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'timetable')
    fields = ('name', 'timetable')
    list_filter = ('timetable__id',)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'starttime', 'endtime', 'timetable')
    fields = ('number', 'starttime', 'endtime', 'timetable')
    list_filter = ('timetable__id',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'classroom', 'teacher',
                    'group', 'day', 'period', 'timetable')
    fields = ('subject', 'classroom', 'teacher',
              'group', 'day', 'period', 'timetable')
    search_fields = ('subject', 'classroom', 'teacher',
                     'group', 'day', 'period')
    list_filter = ('timetable__id',)
