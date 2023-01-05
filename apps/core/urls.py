from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from . import views

urlpatterns = [
    path('version/', views.GetLatestAndCreateVersion.as_view(),
         name='latest-version'),
    path('openapi', get_schema_view(
        title="Nissenger Backend",
        description='API that fetches data from <a href="https://fmalmnis.edupage.org/">https://fmalmnis.edupage.org/</a>',
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger'),
]
