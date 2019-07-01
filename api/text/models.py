from django.db import models
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from typing import List

from text.state import TranslationAssigned, TranslationRefused, WaitingReview, Reviewing, ToFinish, Finished


CHOICES = (
    ('1', 'To translate'),
    ('2', 'Translating'),
    ('3', 'To review'),
    ('4', 'Reviewing'),
    ('5', 'To finish'),
    ('6', 'Finished')
)

LEVELS = (
    ('1', 'Low'),
    ('2', 'Average'),
    ('3', 'High'),
)

""" Text."""


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, null=False, blank=False)
    category_description = models.CharField(max_length=200, null=False,
                                            blank=False)


class TextComponent(models.Model):

    def get_price(self) -> float:
        pass

    def get_content(self) -> str:
        pass

    class Meta:
        abstract = True


class Text(TextComponent):
    total_fragments = models.IntegerField(default=0)
    fragments_done = models.IntegerField(default=0)
    fragments_revision = models.IntegerField(default=0)
    fragments_doing = models.IntegerField(default=0)
    context = models.CharField(max_length=200, null=False, blank=False)
    author = models.CharField(max_length=50, null=False, blank=False)
    language = models.IntegerField(null=False, blank=False)
    categories = models.ManyToManyField(Category)
    translated_text = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=7, choices=LEVELS,
                             default='1', null=False, blank=False)

    def init(self) -> None:
        self.children: List[TextComponent] = []

    def add(self, text_component) -> None:
        self.children.append(text_component)

    def sort_fragments(self) -> None:
        self.children.sort(key=lambda x: x.position)

    def get_price(self) -> float:
        price = 0
        for i in self.children:
            price += i.get_price()
        return price

    def get_content(self) -> str:
        translated_text = ""
        for i in self.children:
            translated_text += i.get_content() + " "

        return translated_text
        
    def save_fragments(self) -> None:
        position = 1
        for i in self.children:
            i.position = position
            i.save()
            position += 1


""" Fragment."""


class TextFragment(TextComponent):
    text = models.ForeignKey(Text, on_delete=models.SET_NULL,
                             null=True)
    body = models.TextField(null=False, blank=False)
    price = models.FloatField(default=0)
    state = models.CharField(max_length=12, choices=CHOICES,
                             default='1', null=False, blank=False)
    total_reviews = models.IntegerField(default=0)
    position = models.IntegerField(blank=True, null=True)
    translated_fragment = models.TextField(default="", blank=True, null=True)
    fragment_translator = models.CharField(max_length=50, null=True,
                                           blank=True)
    total_words = models.IntegerField(blank=True)

    def get_type(self) -> str:
        return 'text'

    def get_price(self) -> float:
        return self.price

    def get_content(self) -> str:
        return str(self.translated_fragment)

    def notify_observers(self, next_state):
        oberserver_author = ConcreteObserverAuthor()
        oberserver_translator = ConcreteObserverTranslator()
        oberserver_revisor = ConcreteObserverRevisor()
        list_observer = [oberserver_author, oberserver_revisor, oberserver_translator]

        for i in list_observer:
            i.notify(self, self.state, next_state)
    
    def change_state(self, next_state):
        state = None
        if next_state == '2':
            state = TranslationAssigned()
        elif next_state == '2.1':
            state = TranslationRefused()
        elif next_state == '3':
            state = WaitingReview()
        elif next_state == '4':
            state = Reviewing()
        elif next_state == '5':
            state = ToFinish()
        elif next_state == '6':
            state = Finished()

        if state:
            state.change_state(self)

""" Review."""


class Review(models.Model):
    fragment = models.ForeignKey(TextFragment, on_delete=models.SET_NULL,
                                 null=True)
    review_username = models.CharField(max_length=50, null=False, blank=False)
    comment = models.TextField(blank=True, null=True)
    approve = models.BooleanField(default=False)


""" Notification """

class Observer(models.Model):

    observer_type = models.CharField(max_length=50, default='Nada')

    def notify(self, fragment, previous_state, actual_state) -> None:
        pass

    class Meta:
        abstract = True


class ConcreteObserverAuthor(Observer):

    observer_type = "Author"

    def notify(self, fragment, previous_state, actual_state) -> None:
        message = "empty"
        if (previous_state == '1') and (actual_state == '2'):
            message = "One of your fragments have been assigned!"
        elif (previous_state == '3') and (actual_state == '4'):
            message = "Almost done! One of your fragments is being reviewed!"
        elif (previous_state == '5') and (actual_state == '6'):
            message = "Building up! A Fragment translation is complete!"
        else:
            return
        parent_text = fragment.text

        notification = Notification()
        notification.text_id = fragment.text
        notification.target_username = parent_text.author
        notification.message = message

        notification.save()



class ConcreteObserverTranslator(Observer):

    observer_type = "Translator"

    def notify(self, fragment, previous_state, actual_state) -> None:
        message = "empty"
        if (previous_state == '3') and (actual_state == '4'):
            message = "Your Translation is being reviewed!"
        elif (previous_state == '4') and (actual_state == '1'):
            message = "Oops! There are some corrections to make on your translation."
        else:
            return

        notification = Notification()
        notification.text_id = fragment.text
        notification.target_username = fragment.fragment_translator
        notification.message = message

        notification.save()



class ConcreteObserverRevisor(Observer):

    observer_type = "Revisor"

    def notify(self, fragment, previous_state, actual_state) -> None:
        message = "empty"
        if (previous_state == '5') and (actual_state == '6'):
            message = "Hooray! One of your reviews got accepted!"
        else:
            return
        # parent_fragment = TextFragment.objects.get(id=fragment_id)
        reviews = []
        try:
            reviews = Review.objects.all().filter(fragment=fragment.id)
            print(reviews)

        except Review.DoesNotExist:
            return

        for review in reviews:
            notification = Notification()
            notification.text_id = fragment.text
            notification.target_username = review.review_username
            notification.message = message
            notification.save()



class Notification(models.Model):
    text_id = models.ForeignKey(Text, on_delete=models.SET_NULL,null=True)
    target_username = models.CharField(max_length=50, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    is_seen = models.BooleanField(default=False)

# @receiver(post_save, sender=settings.REVIEW_FRAGMENT_DB)
# def create_fragment_validator(sender, instance=None,
#                               created=False, **kwargs):
#     """
#     Verify if the same review is the translator, and don't permit if the same
#     reviewer get more than 30% of fragments.
#     """
#     fragment = self.request.
