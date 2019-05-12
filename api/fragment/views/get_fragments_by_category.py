from fragment.models import Fragment
from fragment.serializers import FragmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class GetFragmentsByCategory(APIView):

    def get(self, request, id_category):
        fragments = Fragments.objects.filter(category = id_category)
        serializer = FragmentSerializer(fragments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
