from django.contrib import admin
from text.models import (
    Text,
    Category,
    TextFragment,
    Review
)

admin.site.register(Text)
admin.site.register(TextFragment)
admin.site.register(Category)
admin.site.register(Review)
