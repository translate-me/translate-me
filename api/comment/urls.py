from django.urls import path
from comment.views import CommentView

urlpatterns = [
    path('', CommentView.as_view()),
]
