from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from fragment.models import Fragment
from text.models import Text
from text.serializers import TextSerializer
from rest_framework import viewsets
from rest_framework.decorators import action



class FragmentView(viewsets.ViewSet):
    @action(detail=True, methods=['get'])
    def get_fragments_by_text_id(self, request):
        id_text = request.data['id_text']
        text = Text.objects.get(id = id_text)
        fragments = Fragment.objects.filter(id_text= text)
        return Response("ok")




# Create your views here.
