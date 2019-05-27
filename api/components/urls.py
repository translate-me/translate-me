from django.urls import path
from .views import GetAllFragments

urlpatterns = [
    path('', GetAllFragments.as_view()),
]
