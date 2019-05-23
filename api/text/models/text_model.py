from django.db import models


class Text (models.Model):
    context = models.CharField(max_length=200)
    total_fragments = models.IntegerField(default=0)
    finished_fragments = models.IntegerField(default=0)
    author = models.CharField(max_length=50)
    language = models.IntegerField()
