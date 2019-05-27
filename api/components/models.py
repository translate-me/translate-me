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

class TextComponent(models.Model):

    def init(self) -> None:
        pass

    def add(self, text_compoment) -> None:
        pass
    
    def get_type(self) -> str:
        pass

    def get_fragments(self) -> []:
        pass

    class Meta:
        abstract = True


class TextComposite (TextComponent):
    context = models.CharField(max_length=200)
    total_fragments = models.IntegerField(default=0)
    finished_fragments = models.IntegerField(default=0)
    author = models.IntegerField() #id_autor

    def init(self) -> None:
        self.children: List[TextComponent] = []

    def add(self, text_component) -> None:
        self.children.append(text_component)

    def get_fragments(self) -> str:
        self.children.sort(key=lambda x: x.position) 
        return self.children
    
    def save_db(self) -> None:
        position = 1
        for i in self.children:
            i.position = position
            i.save()
            position += 1


class TextFragment(TextComponent):
    position = models.IntegerField(blank=True, null=True)
    text = models.ForeignKey(TextComposite, on_delete=models.CASCADE)
    content = models.TextField()
    translated = models.TextField()
    value = models.FloatField(default=0)
    state = models.CharField(max_length=12, choices=CHOICES, default='1')
    total_reviews = models.IntegerField(default=0)

    def get_type(self) -> str:
        return 'text'


class ImageFragment(TextComponent):
    position = models.IntegerField(blank=True, null=True)
    text = models.ForeignKey(TextComposite, on_delete=models.CASCADE)
    image = models.TextField()

    def get_type(self) -> str:
        return 'image'

