from django.db import models
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
    fragment_translate = models.TextField(null=True, blank=True)

    def get_type(self) -> str:
        return 'text'
    
    def get_price(self) -> float:
        return self.price


""" Review."""


class Review(models.Model):
    fragment = models.ForeignKey(TextFragment, on_delete=models.SET_NULL,
                                    null=True)
    review_username = models.CharField(max_length=50, null=False, blank=False)
    comment = models.TextField()
    approve = models.BooleanField(default=False)
