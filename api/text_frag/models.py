from django.db import models

CHOICES = [
    (1, 'To correct'),
    (2, 'Correcting'),
    (3, 'To review'),
    (4, 'Reviewing'),
    (5, 'To finish'),
    (6, 'Finished')
]

# Create your models here.
class TextFrag (models.Model):
    content = models.CharField(max_length=20000)
    value = models.FloatField(default=0)
    state = models.CharField(max_length=1, choices=CHOICES, default=1)
    total_reviews = models.IntegerField(default=0)
    # idTexto aqui
        