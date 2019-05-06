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
        '''
        Receives a JSON and processes its content
        '''
        
        text_content = self.request.data['text_content']
        breakpoints = self.request.data['breakpoints']
        self.fragment_text(text_content, breakpoints)

        return Response("Fragmentos criados", status=status.HTTP_201_CREATED)

    def fragment_text(self, text_content, breakpoints):
        '''
        Receives a text and splits it into fragments, according to breakpoints
        '''

        break_point = 0
        for i in breakpoints:
            fragment_content = text_content[break_point:i]
            break_point = i
            self.create_fragment(fragment_content)
        last_fragment_content = text_content[break_point:]
        self.create_fragment(last_fragment_content)
    
    def create_fragment(self, fragment_content):
        '''
        Receives a fragment and saves it in database
        '''

        fragment = TextFrag.objects.create(
            content = fragment_content,
            value = len(fragment_content)*0.1,
        ) 
        
# {
#     "text_content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
#     "breakpoints": [50, 100, 150, 250, 400, 500]
# }

