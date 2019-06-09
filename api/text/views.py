from text.permissions import ServiceAuthenticationDjango
from rest_framework import serializers
from text.utils import (
    FragmentIterator,
    percent_of_fragments,
)
from text.messages import Messages
from rest_framework import generics
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAdminUser,
)
from text.models import (
    Category,
    Text,
    TextFragment,
    Review,
    Observer,
    ConcreteObserverAuthor,
    Notification,
)
from text.serializers import (
    # Serializer category
    CategorySerializerAddAndUpdate,
    CategorySerializerList,
    # Serializer Text
    TextSerializerAddAndUpdate,
    TextSerializerList,
    # Serializer Fragment
    TextFragmentSerializerAddAndUpdate,
    TextFragmentSerializerList,
    TextFragmentAddTranslatorSerializer,
    # Serializer Review
    ReviewSerializerAddAndUpdate,
    ReviewSerializerList,
    # Serializer Notification
    NotificationSerializer,
)

MESSAGES = Messages()

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
        serializer.save()
        fragments = data['fragments']
        id_text = serializer.data['id']
        text = Text.objects.get(id=id_text)
        text.init()
        try:
            _ = [done for done in FragmentIterator(fragments, text)]
        except Exception as erro:
            raise serializers.ValidationError(erro)
        text.save_fragments()
        return JsonResponse({'status': True,
                             'message': MESSAGES.SUCESS_SAVE_TEXT})


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
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentSerializerAddAndUpdate


# List class
class ListFragments(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentSerializerList
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'text__language', 'text__categories')


# Update, detail, patch and destroy class
class UpdateDestroyListFragment(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentSerializerAddAndUpdate

    def perform_update(self, serializer):
        data = self.request.data
        fragment_id = self.kwargs['pk']
        next_state = data['state']
        instanced_fragment = TextFragment.objects.get(id=fragment_id)
        instanced_fragment.notify_observers(next_state)
        serializer.save()

class FragmentTranslatorRelation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentAddTranslatorSerializer

    def perform_update(self, serializer):
        """
        Verify fragment's percent can person allow to get.
        """
        data = self.request.data
        if not percent_of_fragments(data['fragment_translator'],
                                    data['text']):
            raise serializers.ValidationError(MESSAGES.ERROR_MORE_THAN_30)
        serializer.save()


class FragmentToReview(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextFragmentSerializerList

    def get_queryset(self):
        """
        Filter queryset to not get fragments with the same translator and
        author to review.
        """
        username = self.kwargs['username']
        texts = Text.objects.filter(author=username)
        id_texts = [text.id for text in texts]
        fragments = TextFragment.objects.exclude(
            fragment_translator=username
        ).exclude(
            text__in=id_texts
        )
        return fragments


""" Review."""


# Create class
class AddNewReview(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerAddAndUpdate

    def perform_create(self, serializer):
        """
        Verify if reviewer can get the fragment.
        """
        instance = serializer.data
        fragment = TextFragment.objects.get(id=instance['fragment'])
        translator = fragment.fragment_translator
        text_author = fragment.text.author
        # The translator and review is the same
        if instance['review_username'] == translator:
            raise serializers.ValidationError(MESSAGES.ERRO_SAME_USER)
        # The review and author is the same
        if instance['review_username'] == text_author:
            raise serializers.ValidationError(MESSAGES.ERRO_SAME_AUTHOR)
        serializer.save()





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

# List Notification
class ListNotification(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# Update, detail, patch and destroy class
class UpdateDestroyListNotification(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
