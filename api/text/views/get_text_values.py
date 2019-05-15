from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from text.models.fragment_model import Fragment
from text.models.text_model import Text
from text.serializers.values_serializer import ValuesSerializer

# Create your views here.

class GetTextValues(APIView):
    def get(self, request, text_id):
        amount_fragments = Text.objects.filter(id = text_id).values('total_fragments')
        fragments_list = Fragment.objects.filter(text__id = text_id)
        total_words = 0 #Total amount of words at all fragments

        for i in fragments_list:
            fragment_content = i.content
            total_words = total_words + self.count_words(fragment_content)

        print(total_words)

        values = Values(total_words)
        serializer = ValuesSerializer(values)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def count_words(self, fragment_content):
        return len(fragment_content.split(' ')) #get the amount of words for each fragment



class Values(object):
    def __init__(self, amount_words):
        self.amount_words = amount_words
