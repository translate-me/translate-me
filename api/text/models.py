from django.db import models
from category.models import Category

# Create your models here.

class Text (models.Model):
    context = models.CharField(max_length=200)
    total_fragments = models.IntegerField(default=0)
    finished_fragments = models.IntegerField(default=0)
    author = models.IntegerField() #id_autor
    language = models.IntegerField() #id_language
    category = models.ManyToManyField(Category)
