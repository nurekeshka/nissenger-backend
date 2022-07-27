from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.TeacherList.as_view(), name='list-teachers'),
    path('periods/', views.PeriodList.as_view(), name='list-periods'),
    path('offices/', views.OfficeList.as_view(), name='list-offices'),
    path('classes/', views.ClassList.as_view(), name='list-classes'),
]
