from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.TeacherList.as_view(), name='list-teachers'),
    path('periods/', views.PeriodList.as_view(), name='list-periods'),
    path('classrooms/', views.ClassroomList.as_view(), name='list-classrooms'),
    path('classes/', views.ClassList.as_view(), name='list-classes'),
    path('upload', views.TimetableLoadView.as_view(), name='timetable-upload'),
    path('schools/', views.SchoolList.as_view(), name='list-schools'),
    path('schools/<int:pk>/', views.RetrieveSchool.as_view(), name='get-school'),
    path('lessons/', views.LessonsList.as_view(), name='list-lessons'),
]
