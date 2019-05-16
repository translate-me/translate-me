from django.urls import path
from category.views import CategoryView

urlpatterns = [
    path('', CategoryView.as_view()),
]
