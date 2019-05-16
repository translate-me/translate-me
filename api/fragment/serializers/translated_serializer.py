from rest_framework import serializers
from fragment.models import Fragment


class TranslatedSerializer(serializers.ModelSerializer):


    class Meta:
        model = Fragment
        fields = [
            'translated',
        ]
