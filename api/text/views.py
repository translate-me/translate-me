from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fragment.models import Fragment
from text.models import Text
from text.serializers import TextSerializer

# Create your views here.

class TextView(APIView):
    def get(self, request):
        try:
            data = request.data
            author = data['author']
            texts = Text.objects.filter(author=author)
            serializer = TextSerializer(texts, many=True)
            return Response(serializer.data)
        except:
            return Response('Send me a JSON', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        text_content = data['text_content']
        breakpoints = data['breakpoints']
        serializer = TextSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            self.fragment_text(text_content, breakpoints, serializer.data['id'])
            return Response('Text successfully inserted', status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

    def fragment_text(self, text_content, breakpoints, id_text):
        '''
        Receives a id_text and splits it into fragments, according to breakpoints
        '''

        text = Text.objects.get(id = id_text)
        break_point = 0
        for i in breakpoints:
            fragment_content = text_content[break_point:i]
            break_point = i
            self.create_fragment(fragment_content, text)
        last_fragment_content = text_content[break_point:]
        self.create_fragment(last_fragment_content, text)
        text.total_fragments = len(breakpoints) + 1
        text.save()

    def create_fragment(self, fragment_content, text):
        '''
        Receives a fragment and saves it in database
        '''
        fragment = Fragment.objects.create(
            content = fragment_content,
            value = len(fragment_content)*0.1,
            text = text
        )


# {
#     "text_content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ut tristique ligula. Donec mollis lorem elementum purus semper convallis. Etiam ac lectus ac dolor tempus pellentesque non eu enim. Integer venenatis neque eget massa blandit, iaculis tincidunt tellus egestas. Nunc finibus, elit at sagittis sodales, velit ligula malesuada nulla, eget mollis turpis ipsum sed mi. Cras non condimentum lectus. Suspendisse potenti. Mauris nulla sapien, tempor eget ipsum et, vehicula imperdiet massa. Praesent sed vehicula nulla. Proin sagittis consequat lacus sit amet suscipit. Etiam a risus vel leo venenatis ultricies at semper ante. Maecenas sed odio mauris.",
#     "context": "Hello World",
#     "author": 1,
#     "language": 1,
#     "category": [1],
#     "breakpoints": [50, 100, 150, 250, 400, 500]
# }
