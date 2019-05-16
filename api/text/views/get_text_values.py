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
        total_fragment_values = 0.0
        word_per_fragment_list = []

        for i in fragments_list:
            fragment_content = i.content
            fragment_words = self.count_words(fragment_content) #function to get quantity of words of one fragment
            fragment_value = self.calcule_fragment_value(fragment_words) #function to get price for the fragment



            Fragment.objects.filter(id=i.id).update(value = (fragment_value*0.60)) #Update value of the fragment that each translator should receive
            #revisor_value = fragment_value*10
            total_words = total_words + fragment_words #Update total number of words
            total_fragment_values = total_fragment_values + fragment_value #Update total fragments value
            word_per_fragment_list.append(fragment_words)

        values = Values(total_words, total_fragment_values)
        serializer = ValuesSerializer(values)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def count_words(self, fragment_content):
        parcial_words = len(fragment_content.split(' ')) #get the amount of words for each fragment
        return parcial_words

    def calcule_fragment_value(self, fragment_words):
        fragment_value = (fragment_words * 0.20) #Amount of money charged per word
        return fragment_value

    # def calcule_security_level(self, word_per_fragment_list): ############### ASK PO
    #     # for x in word_per_fragment_list:
    #     #     if x <= 200


class Values(object):
    def __init__(self, amount_words, total_price):
        self.amount_words = amount_words
        self.total_price = total_price
