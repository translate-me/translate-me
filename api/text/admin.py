from django.contrib import admin
from text.models.text import Text
from text.models.fragment import Fragment

# Register your models here.
admin.site.register(Text)
admin.site.register(Fragment)
