from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.TeacherList.as_view(), name='list-teachers')
]
