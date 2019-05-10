from django.contrib import admin
from text.models.text_model import Text
from text.models.fragment_model import Fragment

# Register your models here.
admin.site.register(Text)
admin.site.register(Fragment)
