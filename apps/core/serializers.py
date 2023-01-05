from rest_framework import serializers

from . import models


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Version
        fields = ('major', 'minor', 'patch')
