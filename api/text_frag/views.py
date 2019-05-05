from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from text_frag.models import TextFrag
from text_frag.serializers import TextFragSerializer

# Create your views here.

class TextFragView(APIView):
    def get(self, request):
        return Response('ok')

    def post(self, request):
        text_content = self.request.data['text_content']
        breakpoints = self.request.data['breakpoints']
        text_lenght = len(text_content)

        for i in range(len(breakpoints)-1):
            text_aux = text_content
            text_aux = text_content[breakpoints[i]:breakpoints[i+1]]

        text_aux = text_content[breakpoints[-1]:text_lenght]

        return Response(text_content, status=status.HTTP_201_CREATED)
        

# {
#     "text_content": "hello, world",
#     "breakpoints": [0, 6, 9]
# }

