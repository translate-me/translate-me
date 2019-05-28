from django.db import models
# MAX_LENGTH_CHAR = 10 * 1024 * 1024
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
    category_name = models.CharField(max_legth=100)
    category_description = models.CharField(max_legth=200)


class Text(models.Model):
    body = models.TextField()
    total_fragments = models.IntegerField(default=0)
    fragments_done = models.IntegerField(default=0)
    fragments_revision = models.IntegerField(default=0)
    fragments_doing = models.IntegerField(default=0)
    context = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    language = models.IntegerField()


class Have(models.Model):
    class Meta:
        unique_together = ('category_id', 'text_id')

    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                    null=False, blank=False)
    text_id = models.ForeignKey(Text, on_delete=models.SET_NULL,
                                null=False, blank=False)


""" Fragment."""


class Fragment(models.Model):
    text_id = models.ForeignKey(Text, on_delete=models.SET_NULL)
    body = models.TextField()
    price = models.FloatField(default=0)
    state = models.CharField(max_legth=12, choices=CHOICES,
                             default='To translate')
    review_username = models.CharField(max_length=50, null=True, blank=True)
    total_reviews = models.IntegerField(default=0)
