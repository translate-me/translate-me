from django.urls import path
from fragment.views import FragmentView

urlpatterns = [
    path('', FragmentView.as_view()),
]
