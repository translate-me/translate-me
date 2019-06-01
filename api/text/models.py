from django.db import models
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


class Text(models.Model):
    body = models.TextField(null=False, blank=False)
    total_fragments = models.IntegerField(default=0)
    fragments_done = models.IntegerField(default=0)
    fragments_revision = models.IntegerField(default=0)
    fragments_doing = models.IntegerField(default=0)
    context = models.CharField(max_length=200, null=False, blank=False)
    author = models.CharField(max_length=50, null=False, blank=False)
    language = models.IntegerField(null=False, blank=False)
    categories = models.ManyToManyField(Category)
    text_translate = models.TextField(null=True, blank=True)


""" Fragment."""


class Fragment(models.Model):
    text_id = models.ForeignKey(Text, on_delete=models.SET_NULL,
                                null=True)
    body = models.TextField(null=False, blank=False)
    price = models.FloatField(default=0)
    state = models.CharField(max_length=12, choices=CHOICES,
                             default='To translate', null=False, blank=False)
    total_reviews = models.IntegerField(default=0)
    fragment_translate = models.TextField(null=True, blank=True)


""" Review."""


class Review(models.Model):
    fragment_id = models.ForeignKey(Fragment, on_delete=models.SET_NULL,
                                    null=True)
    review_username = models.CharField(max_length=50, null=False, blank=False)
    comment = models.TextField()
    approve = models.BooleanField(default=False)
