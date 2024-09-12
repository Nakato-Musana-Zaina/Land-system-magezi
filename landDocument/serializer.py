from rest_framework import serializers
from landDocument.models import LandDocument


class LandDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandDocument
        fields = '__all__'
