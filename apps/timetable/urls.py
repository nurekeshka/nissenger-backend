from django.urls import path
from . import views

urlpatterns = [
    path('search-class/', views.SearchClass.as_view(), name='search-class'),
    path('search-group/', views.SearchGroup.as_view(), name='search-group'),
    path('upload', views.TimetableLoadView.as_view(), name='timetable-upload'),
    path('schools/', views.SchoolList.as_view(), name='list-schools'),
    path('lessons/', views.LessonsList.as_view(), name='list-lessons'),
    path('teachers/', views.TeachersList.as_view(), name='list-teachers'),
    path('subjects/profile-directed/',
         views.ProfileSubjectsList.as_view(), name='list-profile-subjects'),
]
