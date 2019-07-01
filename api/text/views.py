from text.permissions import ServiceAuthenticationDjango
from rest_framework import serializers
from text.utils import (
    FragmentIterator,
    percent_of_fragments,
    get_all_fragments,
    verify_last_state,
    change_fragments_states
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

from drf_yasg.utils import swagger_auto_schema


MESSAGES = Messages()


""" Category controller."""


# Create class
class AddNewCategory(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerAddAndUpdate

    @swagger_auto_schema(request_body=CategorySerializerAddAndUpdate,
                         response={200: CategorySerializerAddAndUpdate},
                         operation_description="Add new category"
    )
    def perform_create(self, serializer):
        serializer.save()

# List class
class ListCategories(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerList

    @swagger_auto_schema(request_body=CategorySerializerList,
                         response={200: CategorySerializerList},
                         operation_description="List categories"
    )
    def perform_create(self, serializer):
        serializer.save()


# Update, detail, patch and destroy class
class UpdateDestroyListCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Category.objects.all()
    serializer_class = CategorySerializerList

    @swagger_auto_schema(request_body=CategorySerializerList,
                         response={200: CategorySerializerList},
                         operation_description="Update/Destroy categories"
    )
    def perform_create(self, serializer):
        serializer.save()


""" Text controller"""

# Create class
class AddNewText(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Text.objects.all()
    serializer_class = TextSerializerAddAndUpdate

    @swagger_auto_schema(request_body=TextSerializerAddAndUpdate,
                         response={200: TextSerializerAddAndUpdate},
                         operation_description="Add new text"
    )

    def perform_create(self, serializer):
        data = self.request.data
        text = serializer.save()
        fragments = data['fragments']
        # id_text = serializer.data['id']
        # text = Text.objects.get(id=id_text)
        text.init()
        try:
            _ = [done for done in FragmentIterator(fragments, text)]
        except Exception as erro:
            raise serializers.ValidationError(erro)
        text.total_fragments = len(fragments)
        text.save()
        text.save_fragments()
        return JsonResponse({'status': True,
                             'message': MESSAGES.SUCESS_SAVE_TEXT})


class ListTexts(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextSerializerList
    queryset= Text.objects.all()

    @swagger_auto_schema(request_body=TextSerializerList,
                         response={200: TextSerializerList},
                         operation_description="List text"
    )
    def perform_create(self, serializer):
        serializer.save()

# List translated text
class ListTranslatedText(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextSerializerList
    
    @swagger_auto_schema(request_body=TextSerializerList,
                         response={200: TextSerializerList},
                         operation_description="List translated text"
    )

    def get_queryset(self):
        id_text = self.kwargs['id_text']
        text = Text.objects.get(id=id_text)

        get_all_fragments(text)
        text.translated_text = text.get_content()
        text.save()
        return [text]

# List class
class ListTextsByAuthor(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextSerializerList

    @swagger_auto_schema(request_body=TextSerializerList,
                         response={200: TextSerializerList},
                         operation_description="List text by author"
    )


    def get_queryset(self):
        author = self.kwargs['author']
        texts = Text.objects.filter(author=author)
        return texts


# Update, detail, patch and destroy class
class UpdateDestroyListText(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Text.objects.all()
    serializer_class = TextSerializerList

    @swagger_auto_schema(request_body=TextSerializerList,
                         response={200: TextSerializerList},
                         operation_description="Update/Destroy Text"
    )
    def perform_create(self, serializer):
        serializer.save()

""" Fragment."""


# Create class
class AddNewFragment(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentSerializerAddAndUpdate

    @swagger_auto_schema(request_body=TextFragmentSerializerAddAndUpdate,
                         response={200: TextFragmentAddTranslatorSerializer},
                         operation_description="Add new fragment"
    )
    def perform_create(self, serializer):
        serializer.save()


# List class
class GenericListFragments(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextFragmentSerializerList
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="List generic fragments"
    )
    def perform_create(self, serializer):
        serializer.save()

class ListFragmentsByText(GenericListFragments):
    """
    Filter fragments by text id
    """
    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="List fragment by text"
    )
    def perform_create(self, serializer):
        serializer.save()

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

    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="List generic fragments"
    )
    def perform_create(self, serializer):
        serializer.save()

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

    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="List translator of fragments"
    )
    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = TextFragment.objects.filter(
            fragment_translator=username
        )
        return queryset

class FragmentToReview(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    serializer_class = TextFragmentSerializerList

    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="List fragments to review"
    )
    def perform_create(self, serializer):
        serializer.save()

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

class FragmentTranslatorRelation(generics.UpdateAPIView):
    """
    Assign translator relation to fragment
    """
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentAddTranslatorSerializer

    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="Fragments translator relation"
    )
    def perform_update(self, serializer):
        """
        Verify fragment's percent can person allow to get.
        """
        fragment = TextFragment.objects.get(id=self.kwargs['pk'])
        translator = serializer.validated_data['fragment_translator']
        if not percent_of_fragments(translator, fragment.text):
            raise serializers.ValidationError(MESSAGES.ERROR_MORE_THAN_30)
        fragment = serializer.save()
        fragment.change_state('2')
        fragment.save()

class FragmentTranslatorTranslationRefused(generics.UpdateAPIView):
    """
    Ends translator relation to fragment
    """
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentAddTranslatorSerializer

    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="Translator translation refused"
    )

    def perform_update(self, serializer):
        serializer.validated_data['fragment_translator'] =  None
        fragment = serializer.save()
        fragment.translated_fragment = ""
        fragment.change_state('2.1')
        fragment.save()

class FragmentUpdateTranslate(generics.UpdateAPIView):
    """
    Update text that is being translated. Updates it either as a routine or to
    finish the translation
    """
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = TextFragment.objects.all()
    serializer_class = TextFragmentUpdateTranslate

    @swagger_auto_schema(request_body=TextFragmentSerializerList,
                         response={200: TextFragmentSerializerList},
                         operation_description="Update translate"
    )
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
        status = self.request.data['done']
        if status == True:
            id = self.kwargs['pk']
            fragment = TextFragment.objects.get(id=id)
            fragment.change_state('3')
            fragment.save()


""" Review."""


# Create class

class AcceptReview(generics.CreateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerAddAndUpdate

    @swagger_auto_schema(request_body=ReviewSerializerAddAndUpdate,
                         response={200: ReviewSerializerAddAndUpdate},
                         operation_description="Accept Review"
    )
    def perform_create(self, serializer):
        fragment = serializer.validated_data['fragment']
        username = serializer.validated_data['review_username']
        if fragment.fragment_translator == username:
            raise serializers.ValidationError(MESSAGES.ERRO_SAME_USER)
        elif fragment.text.author == username:
            raise serializers.ValidationError(MESSAGES.ERRO_SAME_AUTHOR)
        fragment.change_state('4')
        fragment.save()
        serializer.save()

class RefuseReview(generics.DestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerList
    
    @swagger_auto_schema(request_body=ReviewSerializerList,
                         response={200: ReviewSerializerList},
                         operation_description="Accept Review"
    )

    def perform_destroy(self, serializer):
        revision = Review.objects.get(id=self.kwargs['pk'])
        fragment = revision.fragment
        fragment.change_state('3')
        fragment.save()
        revision.delete()

class UpdateReview(generics.UpdateAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerAddAndUpdate

    @swagger_auto_schema(request_body=ReviewSerializerAddAndUpdate,
                         response={200: ReviewSerializerAddAndUpdate},
                         operation_description="Update Review"
    )

    def perform_update(self, serializer):
        status = self.request.data['done']
        review = serializer.save()
        fragment = review.fragment
        text = fragment.text
        if status == True:
            if review.approve == True:
                fragment.change_state('5')
                text.fragments_done += 1
                text.save()
            else:
                fragment.change_state('2')
            fragment.total_reviews += 1
            fragment.save()

            if verify_last_state(text):
                change_fragments_states(text)
                text.translated_text = text.get_content()
                text.save()


# List class
class ListReviews(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerList

    @swagger_auto_schema(request_body=ReviewSerializerList,
                         response={200: ReviewSerializerList},
                         operation_description="List Review"
    )
    def perform_create(self, serializer):
        serializer.save()


# Update, detail, patch and destroy class
class UpdateDestroyListReview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerList

    @swagger_auto_schema(request_body=ReviewSerializerList,
                         response={200: ReviewSerializerList},
                         operation_description="Update/Destroy Review"
    )
    def perform_create(self, serializer):
        serializer.save()

""" Notification."""

# List Notification
class ListNotification(generics.ListAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @swagger_auto_schema(request_body=NotificationSerializer,
                         response={200: NotificationSerializer},
                         operation_description="List Notification"
    )
    def perform_create(self, serializer):
        serializer.save()

# Update, detail, patch and destroy class
class UpdateDestroyListNotification(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ServiceAuthenticationDjango]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    @swagger_auto_schema(request_body=NotificationSerializer,
                         response={200: NotificationSerializer},
                         operation_description="Update/Destroy Notification"
    )
    def perform_create(self, serializer):
        serializer.save()