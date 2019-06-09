from django.db import models
import json
from typing import List


CHOICES = (
    ('1', 'To translate'),
    ('2', 'Translating'),
    ('3', 'To review'),
    ('4', 'Reviewing'),
    ('5', 'To finish'),
    ('6', 'Finished')
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
    text_translate = models.TextField(null=True, blank=True)


    def init(self) -> None:
        self.children: List[TextComponent] = []

    def add(self, text_component) -> None:
        self.children.append(text_component)

    def get_fragments(self) -> str:
        self.children.sort(key=lambda x: x.position)
        return self.children

    def get_price(self) -> float:
        price = 0
        for i in self.children:
            price += i.get_price()
        return price

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
                             default='To translate', null=False, blank=False)
    total_reviews = models.IntegerField(default=0)
    position = models.IntegerField(blank=True, null=True)
    translator_username = models.CharField(max_length=50, null=True, blank=True)
    fragment_translate = models.TextField(null=True, blank=True)

    def get_type(self) -> str:
        return 'text'

    def get_price(self) -> float:
        return self.price

        
    def notify_observers(self, next_state):
        oberserver_author = ConcreteObserverAuthor()
        oberserver_translator = ConcreteObserverTranslator()
        oberserver_revisor = ConcreteObserverRevisor()
        list_observer = [oberserver_author, oberserver_revisor, oberserver_translator]

        for i in list_observer:
            i.notify(self.pk, self.state, next_state)



""" Review."""


class Review(models.Model):
    fragment = models.ForeignKey(TextFragment, on_delete=models.SET_NULL,
                                    null=True)
    review_username = models.CharField(max_length=50, null=False, blank=False)
    comment = models.TextField()
    approve = models.BooleanField(default=False)



""" Notification """

class Observer(models.Model):

    observer_type = models.CharField(max_length=50, default='Nada')

    def notify(self, fragment_id, previous_state, actual_state) -> None:
        pass

    class Meta:
        abstract = True


class ConcreteObserverAuthor(Observer):

    observer_type = "Author"

    def notify(self, fragment_id, previous_state, actual_state) -> None:
        message = "empty"
        if (previous_state == '1') and (actual_state == '2'):
            message = "One of your fragments have been assigned!"
        elif (previous_state == '3') and (actual_state == '4'):
            message = "Almost done! One of your fragments is being reviewed!"
        elif (previous_state == '5') and (actual_state == '6'):
            message = "Building up! A Fragment translation is complete!"
        else:
            return
        parent_fragment = TextFragment.objects.get(id=fragment_id)
        parent_text = parent_fragment.text

        notification = Notification()
        notification.text_id = parent_fragment.text
        notification.target_username = parent_text.author
        notification.message = message

        notification.save()
        


class ConcreteObserverTranslator(Observer):

    observer_type = "Translator"

    def notify(self, fragment_id, previous_state, actual_state) -> None:
        message = "empty"
        if (previous_state == '3') and (actual_state == '4'):
            message = "Your Translation is being reviewed!"
        elif (previous_state == '4') and (actual_state == '1'):
            message = "Oops! There are some corrections to make on your translation."
        else:
            return
        parent_fragment = TextFragment.objects.get(id=fragment_id)

        notification = Notification()
        notification.text_id = parent_fragment.text
        notification.target_username = parent_fragment.translator_username
        notification.message = message

        notification.save()
        


class ConcreteObserverRevisor(Observer):

    observer_type = "Revisor"

    def notify(self, fragment_id, previous_state, actual_state) -> None:
        message = "empty"
        if (previous_state == '5') and (actual_state == '6'):
            message = "Hooray! One of your reviews got accepted!"
        else:
            return
        parent_fragment = TextFragment.objects.get(id=fragment_id)
        parent_review = None
        try:
            parent_review = Review.objects.get(fragment=fragment_id)
            print(parent_review)

        except Review.DoesNotExist:
            return

        notification = Notification()
        notification.text_id = parent_fragment.text
        notification.target_username = parent_review.review_username
        notification.message = message
        notification.save()
        





class Notification(models.Model):
    text_id = models.ForeignKey(Text, on_delete=models.SET_NULL,null=True)
    target_username = models.CharField(max_length=50, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    is_seen = models.BooleanField(default=False)
