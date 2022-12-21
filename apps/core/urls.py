from django.urls import path
from . import views

urlpatterns = [
    path('version/', views.GetLatestAndCreateVersion.as_view(),
         name='latest-version'),
]
