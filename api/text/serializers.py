from rest_framework import serializers
from text.models import (
    Category,
    Text,
    Have,
    Fragment,
)

""" Category."""


class CategorySerializerAddAndUpdate(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'category_name',
            'category_description'
        ]


class CategorySerializerList(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


""" Text."""


class TextSerializerAddAndUpdate(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = [
            'body',
            'total_fragments',
            'fragments_done',
            'fragments_revision',
            'fragments_doing',
            'context',
            'author',
            'language'
        ]


class TextSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


""" Have."""


class HaveSerializerAddAndUpdate(serializers.ModelSerializer):
    class Meta:
        model = Have
        fields = [
            'category_id',
            'text_id'
        ]


class HaveSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Have
        fields = "__all__"


""" Fragment."""


class FragmentSerializerAddAndUpdate(serializers.ModelSerializer):
    class Meta:
        model = Fragment
        fields = [
            'text_id',
            'body',
            'price',
            'state',
            'review_username',
            'total_reviews'
        ]


class FragmentSerializerList(serializers.ModelSerializer):
    class Meta:
        models = Fragment
        fields = "__all__"
