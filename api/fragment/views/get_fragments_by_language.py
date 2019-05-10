from rest_framework.response import Response
from rest_framework import status
from fragment.models import Fragment
from fragment.serializers import FragmentSerializer
from rest_framework.views import APIView


class GetFragmentsByLanguage(APIView):

    def get(self, request, language_id):        
        fragments = Fragment.objects.filter(text__language = language_id)
        serializer = FragmentSerializer(fragments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
