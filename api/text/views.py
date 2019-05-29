from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from text.models import Text, Fragment
from text.serializers import TextSerializer, FragmentSerializer
from drf_yasg.utils import swagger_auto_schema

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

class FragmentView(APIView):
    @swagger_auto_schema(request_body=FragmentSerializer,
                         responses={200: "Ok"},
                         operation_description="Translator receives the fragment")
    def patch(self, request, pk):
        print(pk)
        fragment = Fragment.objects.get(id=pk)
        serializer = FragmentSerializer(fragment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response('Fragmento atribuído a tradutor com sucesso', status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# {
#     "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ut tristique ligula. Donec mollis lorem elementum purus semper convallis. Etiam ac lectus ac dolor tempus pellentesque non eu enim. Integer venenatis neque eget massa blandit, iaculis tincidunt tellus egestas. Nunc finibus, elit at sagittis sodales, velit ligula malesuada nulla, eget mollis turpis ipsum sed mi. Cras non condimentum lectus. Suspendisse potenti. Mauris nulla sapien, tempor eget ipsum et, vehicula imperdiet massa. Praesent sed vehicula nulla. Proin sagittis consequat lacus sit amet suscipit. Etiam a risus vel leo venenatis ultricies at semper ante. Maecenas sed odio mauris.",
#     "context": "Hello World",
#     "author": 1,
#     "language": 1
# }
