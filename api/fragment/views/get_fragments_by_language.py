from rest_framework.response import Response
from rest_framework import status
from fragment.models import Fragment
from fragment.serializers import FragmentSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class GetFragmentsByLanguage(APIView):

    @swagger_auto_schema(responses={200: "Ok"},
                        operation_description="ok.")
    def get(self, request, id_language):
        fragments = Fragment.objects.filter(text__language = id_language)
        serializer = FragmentSerializer(fragments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
