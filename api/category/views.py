from django.shortcuts import render
from rest_framework.views import APIView
from category.models import Category
from category.serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class CategoryView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Category successfully inserted!", status=status.HTTP_200_OK)
        else:
            return Response("Invalid JSON", status=status.HTTP_400_BAD_REQUEST)
