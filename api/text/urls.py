from django.urls import path
from text.views import PostTextToFragment

urlpatterns = [
    path('', PostTextToFragment.as_view()),
]
