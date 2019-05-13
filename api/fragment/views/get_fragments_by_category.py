from fragment.models import Fragment
from fragment.serializers import FragmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class GetFragmentsByCategory(APIView):

    def get(self, request, categories):
        try:
            categories = categories.split(',')
            categories_int = []
            for i in categories:
                categories_int.append(int(i))

            fragments = Fragment.objects.filter(text__category__in = categories_int)
            serializer = FragmentSerializer(fragments, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except:
            return Response("Something is wrong", status=status.HTTP_400_BAD_REQUEST)
