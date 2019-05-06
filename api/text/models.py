from django.db import models

# Create your models here.

class Text (models.Model):
    content = models.TextField()
    author = models.CharField(max_length=100)
