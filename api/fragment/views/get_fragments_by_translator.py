from rest_framework.response import Response
from rest_framework import status
from fragment.models import Fragment
from fragment.serializers.fragment_serializer import FragmentSerializer
from rest_framework.views import APIView


class GetFragmentsByTranslator(APIView):

    def get(self, request, id_translator):        
        fragments = Fragment.objects.filter(translator = id_translator)
        serializer = FragmentSerializer(fragments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
