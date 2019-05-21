from rest_framework.response import Response
from rest_framework import status
from fragment.models import Fragment
from fragment.serializers.translated_serializer import TranslatedSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

class PatchTextTranslated(APIView):

    def get(self, request, id_fragment):
        return Response('Page loaded', status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TranslatedSerializer,
                         responses={200: "Ok"},
                         operation_description="Edit translated text")
    def patch(self, request, id_fragment):
        data = request.data
        serializer = TranslatedSerializer(data=data)
        if serializer.is_valid():
            translated_fragment = serializer.data['translated']
            print(translated_fragment)
            Fragment.objects.filter(id = id_fragment).update(translated = translated_fragment)
            return Response('Text Updated', status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

            


# {
#     "translated": "A gente pode testar"
# }

