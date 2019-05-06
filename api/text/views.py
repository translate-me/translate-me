from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from text.models import Text
from text.serializers import TextSerializer

# Create your views here.

class TextView(APIView):
    def get(self, request):
        return Response('ok')

    # def post(self, request):
    #     text_content = self.request.data['text_content']
    #     breakpoints = self.request.data['breakpoints']
    #     text_lenght = len(text_content)
    #
    #     for i in range(len(breakpoints)-1):
    #         fragment_content = text_content[breakpoints[i]:breakpoints[i+1]]
    #         self.create_fragment(fragment_content)
    #
    #     last_fragment_content = text_content[breakpoints[-1]:text_lenght]
    #     self.create_fragment(last_fragment_content)
    #
    #     return Response("Fragmentos criados", status=status.HTTP_201_CREATED)
    #
    # def create_fragment(self, fragment_content):
    #     fragment = TextFrag.objects.create(
    #         content = fragment_content,
    #         value = len(fragment_content)*0.1,
)
