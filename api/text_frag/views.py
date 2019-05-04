from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class TextFragView(APIView):

    def get(self, request):
        return Response('ok')

    def post(self, request):
        return Response('Post Ok')

# [
#     {
#         "conteudo": conteudo
#     }
# ]
