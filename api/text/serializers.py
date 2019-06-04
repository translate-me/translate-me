from rest_framework import serializers
from text.models import (
    Category,
    Text,
    TextFragment,
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
            'id',
            # 'body',
            'total_fragments',
            'fragments_done',
            'fragments_revision',
            'fragments_doing',
            'context',
            'language',
            'categories'
        ]


class TextSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


""" Fragment."""


class TextFragmentSerializerAddAndUpdate(serializers.ModelSerializer):
    class Meta:
        model = TextFragment
        fields = [
            'text_id',
            'body',
            'price',
            'state',
            'review_username',
            'total_reviews'
        ]


class TextFragmentSerializerList(serializers.ModelSerializer):
    class Meta:
        model = TextFragment
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
