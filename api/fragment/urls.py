from django.urls import path
from fragment.views.get_fragments_by_language import GetFragmentsByLanguage
from fragment.views.get_fragments_by_translator import GetFragmentsByTranslator
from fragment.views.get_fragments_by_id_text import GetFragmentsByTextId
from fragment.views.get_all_fragments import GetAllFragments

urlpatterns = [
    path('fragments_by_language/<int:id_language>/', GetFragmentsByLanguage.as_view()),
    path('fragments_by_translator/<int:id_translator>/', GetFragmentsByTranslator.as_view()),
    path('fragments_by_id_text/<int:id_text>/', GetFragmentsByTextId.as_view()),
    path('all_fragments/', GetAllFragments.as_view()),
]
