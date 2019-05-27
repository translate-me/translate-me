from django.contrib import admin
from .models import TextComposite, TextFragment, ImageFragment

# Register your models here.
admin.site.register(TextComposite)
admin.site.register(TextFragment)
admin.site.register(ImageFragment)