from django.urls import path
from fragment.views.get_fragments_by_language import GetFragmentsByLanguage
from fragment.views.get_fragments_by_translator import GetFragmentsByTranslator

urlpatterns = [
    path('fragments_by_language/<int:id_language>/', GetFragmentsByLanguage.as_view()),
    path('fragments_by_translator/<int:id_translator>/', GetFragmentsByTranslator.as_view()),
]
