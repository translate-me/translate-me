from django.urls import path
from text.views import TextView

urlpatterns = [
    path('', TextView.as_view()),
]
