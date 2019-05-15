from django.urls import path
from text.views.post_text_to_fragment import PostTextToFragment
from text.views.get_text_values import GetTextValues

urlpatterns = [
    path('text_to_fragment/', PostTextToFragment.as_view()),
    path('values/<int:text_id>/', GetTextValues.as_view())
]
