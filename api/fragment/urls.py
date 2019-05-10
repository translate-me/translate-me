from django.urls import path
from fragment.views.get_fragments_by_language import GetFragmentsByLanguage

urlpatterns = [
    path('fragments_by_language/<int:language_id>/', GetFragmentsByLanguage.as_view()),
]
