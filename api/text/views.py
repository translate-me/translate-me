from text.permissions import ServiceAuthenticationDjango
from text.utils import FragmentIterator
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.permissions import (
    IsAdminUser,
)
from text.models import (
    Category,
    Text,
    Fragment,
    Review,
    Notification,
    Observer,
    ConcreteObserverAuthor,
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
    # Serializer Notification
    NotificationSerializer,
)


""" Category controller."""


# Create class
class AddNewCategory(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerAddAndUpdate


# List class
class ListCategories(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerList


""" Text controller"""


# Create class
class AddNewText(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Text.objects.all()
    serializer_class = TextSerializerAddAndUpdate

    def perform_create(self, serializer):
        data = self.request.data
        body = data['body']
        breakpoints = data['breakpoints']
        serializer.save()
        id_text = serializer.data['id']
        try:
            _ = [done for done in FragmentIterator(body, breakpoints, id_text)]
            message = "Texto salvo e fragmentado"
            return JsonResponse({'status': True, 'message': message})
        except Exception as erro:
            return JsonResponse({'status': False, 'message': erro})


# List class
class ListTexts(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Text.objects.all()
    serializer_class = TextSerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListText(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Text.objects.all()
    serializer_class = TextSerializerList


""" Fragment."""


# Create class
class AddNewFragment(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Fragment.objects.all()
    serializer_class = FragmentSerializerAddAndUpdate


# List class
class ListFragments(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Fragment.objects.all()
    serializer_class = FragmentSerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListFragment(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Fragment.objects.all()
    serializer_class = FragmentSerializerList


""" Review."""


# Create class
class AddNewReview(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerAddAndUpdate


# List class
class ListReviews(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerList


# Update, detail, patch and destroy class
class UpdateDestroyListReview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerList

""" Notification."""

#List Notification
class ListNotification(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = FragmentSerializerList
    queryset = Fragment.objects.all()

    def perform_update(self, serializer):
        interest_fragment = Fragment.objects.get(id=1)
        interest_fragment.change_state('Translating')
        serializer.save()
    
    # queryset = interest_fragment.observer_list
    




