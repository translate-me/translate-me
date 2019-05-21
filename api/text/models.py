from django.db import models

# Create your models here.

CHOICES = (
    ('1', 'To translate'),
    ('2', 'Translating'),
    ('3', 'To review'),
    ('4', 'Reviewing'),
    ('5', 'To finish'),
    ('6', 'Finished')
)

class Text (models.Model):
    context = models.CharField(max_length=200, default="")
    total_fragments = models.IntegerField(default=0)
    finished_fragments = models.IntegerField(default=0)
    author = models.IntegerField(null=True) #id_autor
    language = models.IntegerField(null=True) #id_language

class Fragment (models.Model):
    id_text = models.ForeignKey(Text, on_delete=models.CASCADE)
    content = models.TextField()
    value = models.FloatField(default=0)
    state = models.CharField(max_length=12, choices=CHOICES, default='1')
    total_reviews = models.IntegerField(default=0)
    id_author = models.IntegerField(null=True)
    id_translator = models.IntegerField(null=True)
    # idTexto aqui


