from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from text.models import Text
from text.serializers import TextSerializer

# Create your views here.

class TextView(APIView):
    def get(self, request):
        return Response('ok')

    def post(self, request):
        data = request.data
        text = data['text']
        serializer = TextSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('Texto inserido com sucesso', status=status.HTTP_201_CREATED)
        else:
            return Response('Dados inválidos', status=status.HTTP_400_BAD_REQUEST)


# {
#     "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ut tristique ligula. Donec mollis lorem elementum purus semper convallis. Etiam ac lectus ac dolor tempus pellentesque non eu enim. Integer venenatis neque eget massa blandit, iaculis tincidunt tellus egestas. Nunc finibus, elit at sagittis sodales, velit ligula malesuada nulla, eget mollis turpis ipsum sed mi. Cras non condimentum lectus. Suspendisse potenti. Mauris nulla sapien, tempor eget ipsum et, vehicula imperdiet massa. Praesent sed vehicula nulla. Proin sagittis consequat lacus sit amet suscipit. Etiam a risus vel leo venenatis ultricies at semper ante. Maecenas sed odio mauris.",
#     "context": "Hello World",
#     "author": 1,
#     "language": 1
# }
