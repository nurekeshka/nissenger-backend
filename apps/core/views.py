from rest_framework import generics, status, views
from rest_framework.request import Request
from rest_framework.response import Response

from . import models, serializers


class GetLatestAndCreateVersion(generics.CreateAPIView):
    serializer_class = serializers.VersionSerializer

    def get(self, request, *args, **kwargs):
        latest = models.Version.objects.all().order_by(
            '-major', '-minor', '-patch').first()
        serializer = serializers.VersionSerializer(instance=latest)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
