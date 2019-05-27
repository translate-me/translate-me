from rest_framework import serializers
from .models import TextComposite, TextFragment, ImageFragment


class TextCompositeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextComposite
        fields = '__all__'


class TextFragmentSerializer(serializers.ModelSerializer):
    text = TextCompositeSerializer()

    class Meta:
        model = TextFragment
        fields = '__all__'


class ImageFragmentSerializer(serializers.ModelSerializer):
    text = TextCompositeSerializer()

    class Meta:
        model = ImageFragment
        fields = '__all__'