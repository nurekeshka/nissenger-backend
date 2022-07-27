from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.TeacherList.as_view(), name='list-teachers'),
    path('classes/', views.ClassList.as_view(), name='list-classes'),
    path('periods/', views.PeriodList.as_view(), name='list-periods'),
]
