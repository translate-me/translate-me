from django.urls import path, re_path
from text.views import TextView, FragmentView

urlpatterns = [
    path('text/', TextView.as_view()),
    re_path(r'fragment/(?P<pk>\d+)/$', FragmentView.as_view()),

]
