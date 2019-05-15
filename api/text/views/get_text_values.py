from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from text.models.fragment_model import Fragment
from text.models.text_model import Text
from text.serializers.text_serializer import TextSerializer

# Create your views here.

class GetTextValues(APIView):
    def get(self, request, text_id):
        try:
            amount_fragments = Text.objects.filter(id = text_id).values('total_fragments')
            fragments_list = Fragment.objects.self.filter(id_text__id = text_id)
            total_words = 0 #Total amount of words at all fragments

            for i in fragments_list:
                fragment_content = i.content
                self.count_words(total_words, fragment_content)

    def count_words(self, total_words, fragment_content):
        total_words = total_words + fragment_content.split(' ') #get the amount of words for each fragment