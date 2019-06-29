from text.permissions import ServiceAuthenticationDjango
from rest_framework import serializers
from text.utils import (
    FragmentIterator,
    percent_of_fragments,
    get_all_fragments
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
    TextFragmentUpdateTranslate,
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


# List translated text
class ListTranslatedText(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextSerializerList

    def get_queryset(self):
        id_text = self.kwargs['id_text']
        text = Text.objects.get(id=id_text)
        text.init()

        get_all_fragments(text)
        text.translated_text = text.get_content()
        text.save()
        return [text]

# List class
class ListTextsByAuthor(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextSerializerList

    def get_queryset(self):
        author = self.kwargs['author']
        texts = Text.objects.filter(author=author)
        return texts


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
class GenericListFragments(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextFragmentSerializerList
    filter_backends = (DjangoFilterBackend,)

class ListFragmentsByText(GenericListFragments):
    """
    Filter fragments by text id
    """

    def get_queryset(self):
        text_id = self.kwargs['text_id']
        queryset = TextFragment.objects.filter(
            text__id=text_id
        )
        return queryset

class ListAvailableFragments(GenericListFragments):
    """
    List available fragments to translate or review
    """

    filterset_fields = ('text__language', 'text__categories', 'text__level')

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = TextFragment.objects.exclude(
            fragment_translator=username
        ).exclude(
            text__author=username
        )
        return queryset

class ListTranslatorFragments(GenericListFragments):
    """
    List all fragments a translator is translating
    """

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = TextFragment.objects.filter(
            fragment_translator=username
        )
        return queryset

# Update, detail, patch and destroy class
class UpdateDestroyListFragment(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentSerializerAddAndUpdate

    def perform_update(self, serializer):
        fragment_id = self.kwargs['pk']
        next_state = self.request.data['state']
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
        fragment_id = self.kwargs['pk']
        instanced_fragment = TextFragment.objects.get(id=fragment_id)
        text_id = instanced_fragment.text
        data = self.request.data
        if not percent_of_fragments(data['fragment_translator'],
                                    text_id):
            raise serializers.ValidationError(MESSAGES.ERROR_MORE_THAN_30)
        next_state = data['state']
        
        instanced_fragment.notify_observers(next_state)
        serializer.save()


class FragmentUpdateTranslate(generics.UpdateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentUpdateTranslate

    def perform_update(self, serializer):
        """
        Update text that is being translated, for a routine
        save or for sending the final translation
        """
        fragment_id = self.kwargs['pk']
        next_state = self.request.data['state']
        instanced_fragment = TextFragment.objects.get(id=fragment_id)
        instanced_fragment.notify_observers(next_state)
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
        instance = serializer.validated_data
        fragment = instance['fragment']
        fragment.notify_observers(instance['state'])
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
