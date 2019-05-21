from rest_framework import serializers
from comment.models import Comment

class CommentSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Comment

        fields = [
        'comments'
        ]
