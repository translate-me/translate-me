from rest_framework import serializers
from text.models import (
    Category,
    Text,
    Fragment,
    Review
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
            'language',
            'categories'
        ]


class TextSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


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
        model = Fragment
        fields = "__all__"


""" Review."""


class ReviewSerializerAddAndUpdate(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'fragment_id',
            'review_username',
            'comment',
            'approve'
        ]


class ReviewSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
