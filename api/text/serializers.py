from rest_framework import serializers
from text.models.text import Text

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = [
            'context',
            'author',
            'language'
        ]
