from rest_framework import serializers
from .models import TextFrag

class TextFragSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextFrag
        fields = '__all__'