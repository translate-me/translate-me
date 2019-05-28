from django.contrib import admin
from text.models import (
    Text,
    Category,
    Fragment,
    Have
)

admin.site.register(Text)
admin.site.register(Fragment)
admin.site.register(Category)
admin.site.register(Have)
