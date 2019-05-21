from rest_framework import serializers
from text.models import Text, Fragment

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'
class FragmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fragment
        fields = ['id_translator']


