from django.urls import path
from text_frag.views import TextFragView

urlpatterns = [
    path('', TextFragView.as_view()),
]
