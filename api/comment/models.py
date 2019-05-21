from django.db import models


# Create your models here.

class Comment(models.Model):
    comments = models.TextField()
  #  fragment = models.ForeignKey(Fragment)
    
