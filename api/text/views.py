# import socket
# import requests as rq
# from rest_framework.response import Response
# from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import (
    IsAdminUser,
)
from text.models import (
    Category,
    Text,
    Fragment,
    Review
)
from text.serializers import (
    # Serializer category
    CategorySerializerAddAndUpdate,
    CategorySerializerList,
    # Serializer Text
    TextSerializerAddAndUpdate,
    TextSerializerList,
    # Serializer Fragment
    FragmentSerializerAddAndUpdate,
    FragmentSerializerList,
    # Serializer Review
    ReviewSerializerAddAndUpdate,
    ReviewSerializerList,
)


""" Category controller."""


# Create class
class AddNewCategory(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerAddAndUpdate


# List class
class ListCategories(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerList


""" Text controller"""


# Create class
class AddNewText(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Text.objects.all()
    serializer_class = TextSerializerAddAndUpdate


# List class
class ListTexts(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Text.objects.all()
    serializer_class = TextSerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListText(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Text.objects.all()
    serializer_class = TextSerializerList


""" Fragment."""


# Create class
class AddNewFragment(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Fragment.objects.all()
    serializer_class = FragmentSerializerAddAndUpdate


# List class
class ListFragments(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Fragment.objects.all()
    serializer_class = FragmentSerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListFragment(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Fragment.objects.all()
    serializer_class = FragmentSerializerList


""" Review."""


# Create class
class AddNewReview(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerAddAndUpdate


# List class
class ListReviews(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListReview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerList
