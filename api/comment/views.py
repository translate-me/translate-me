from django.shortcuts import render
from comment.models import Comment
from comment.serializer import CommentSerialzer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



# Create your views here.
class CommentView(APIView):
    def get(self, request):
        # comments = Comment.objects.get(id)
        return Response('ok')

    def post(self, request):
        data = request.data
        # comment_content = data['comment_content']
        serializer = CommentSerialzer(data=data)
        print(data)
        if serializer.is_valid():
            serializer.save()
            return Response('comentario inserido com sucesso', status=status.HTTP_200_OK)
        else:
            return Response('Algo errado', status=status.HTTP_400_BAD_REQUEST)

# {
#     "comments": "Belo coments"
# }