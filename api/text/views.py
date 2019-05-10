from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from text.models.fragment import Fragment
from text.models.text import Text
from text.serializers import TextSerializer

# Create your views here.

class TextView(APIView):
    def get(self, request):
        return Response('ok')

    def post(self, request):
        data = request.data
        text_content = data['text_content']
        breakpoints = data['breakpoints']
        self.fragment_text(text_content, breakpoints)
        serializer = TextSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('Texto inserido com sucesso', status=status.HTTP_201_CREATED)
        else:
            return Response('Dados inválidos', status=status.HTTP_400_BAD_REQUEST)

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

        fragment = Fragment.objects.create(
            content = fragment_content,
            value = len(fragment_content)*0.1,
        )
# {
#     "text_content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ut tristique ligula. Donec mollis lorem elementum purus semper convallis. Etiam ac lectus ac dolor tempus pellentesque non eu enim. Integer venenatis neque eget massa blandit, iaculis tincidunt tellus egestas. Nunc finibus, elit at sagittis sodales, velit ligula malesuada nulla, eget mollis turpis ipsum sed mi. Cras non condimentum lectus. Suspendisse potenti. Mauris nulla sapien, tempor eget ipsum et, vehicula imperdiet massa. Praesent sed vehicula nulla. Proin sagittis consequat lacus sit amet suscipit. Etiam a risus vel leo venenatis ultricies at semper ante. Maecenas sed odio mauris.",
#     "context": "Hello World",
#     "author": 1,
#     "language": 1,
#     "breakpoints": [50, 100, 150, 250, 400, 500]
# }
