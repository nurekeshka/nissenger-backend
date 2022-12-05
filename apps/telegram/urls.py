from django.urls import path
from . import views


urlpatterns = [
    path('notify-admins/', views.NotifyAdmins.as_view(), name='get-class'),
]
