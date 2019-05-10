from rest_framework import serializers
from fragment.models import Fragment
from text.serializers import TextSerializer


class FragmentSerializer(serializers.ModelSerializer):
    text = TextSerializer()

    class Meta:
        model = Fragment
        fields = [
            'id',
            'content',
            'value',
            'text'
        ]
