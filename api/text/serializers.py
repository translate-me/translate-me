from rest_framework import serializers
from text.models import Text

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'
