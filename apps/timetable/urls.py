from django.urls import path
from . import views

urlpatterns = [
    path('get-class/', views.SearchClass.as_view(), name='get-class'),
    path('search-group/', views.SearchGroups.as_view(), name='search-group'),
    path('upload', views.TimetableLoadView.as_view(), name='timetable-upload'),
    path('schools/', views.SchoolList.as_view(), name='list-schools'),
    path('lessons/', views.LessonsList.as_view(), name='list-lessons'),
    path('teachers/', views.TeachersList.as_view(), name='list-teachers'),
    path('lessons/teachers/', views.LessonsListTeachers.as_view(),
         name='list-lessons-for-teacher'),
    path('subjects/foreign-languages/',
         views.ForeignLanguageSubjects.as_view(), name='list-foreign-languages'),
    path('subjects/profile/',
         views.ProfileSubjectsList.as_view(), name='list-profile-subjects'),
    path('groups/profile/', views.ProfileGroupsList.as_view(),
         name='list-profile-groups'),
    path('subjects/mesk/', views.MeskPreparationSubjects.as_view(),
         name='list-mesk-subjects'),
    path('available/', views.Online.as_view(), name='is-available'),
]
