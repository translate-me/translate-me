from django.shortcuts import render
from rest_framework.views import APIView
from category.models import Category
from category.serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema



# Create your views here.
class CategoryView(APIView):

    @swagger_auto_schema(responses={200: "Ok"},
                         operation_description="Add new category")
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CategorySerializer,
                         responses={200: "Ok"},
                         operation_description="Add new category")
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Category successfully inserted!", status=status.HTTP_200_OK)
        else:
            return Response("Invalid JSON", status=status.HTTP_400_BAD_REQUEST)
