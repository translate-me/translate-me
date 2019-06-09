from django.conf.urls import url
from text.views import (
    AddNewCategory,
    ListCategories,
    UpdateDestroyListCategory,
    AddNewText,
    ListTexts,
    UpdateDestroyListText,
    AddNewFragment,
    ListFragments,
    UpdateDestroyListFragment,
    AddNewReview,
    ListReviews,
    UpdateDestroyListReview,
    ListNotification,
    UpdateDestroyListNotification,
)

urlpatterns = [
    # Category
    url(r'^api/v0/category/create/$', AddNewCategory.as_view(),
        name="create_new_category"),
    url(r'^api/v0/category/list/$', ListCategories.as_view(),
        name="list_categories"),
    url(r'^api/v0/category/(?P<option>update|delete|detail)/(?P<pk>[0-9]+)$',
        UpdateDestroyListCategory.as_view(),
        name="update_destroy_and_detail_category"),
    # Text
    url(r'^api/v0/text/create/$', AddNewText.as_view(),
        name="create_new_text"),
    url(r'^api/v0/text/list/$', ListTexts.as_view(),
        name="list_texts"),
    url(r'^api/v0/text/(?P<option>update|delete|detail)/(?P<pk>[0-9]+)$',
        UpdateDestroyListText.as_view(),
        name="update_destroy_and_detail_text"),
    # Fragment
    url(r'^api/v0/fragment/create/$', AddNewFragment.as_view(),
        name="create_new_fragment"),
    url(r'^api/v0/fragment/list/$', ListFragments.as_view(),
        name="list_fragments"),
    url(r'^api/v0/fragment/(?P<option>update|delete|detail)/(?P<pk>[0-9]+)$',
        UpdateDestroyListFragment.as_view(),
        name="update_destroy_and_detail_fragment"),
    # Review
    url(r'^api/v0/review/create/$', AddNewReview.as_view(),
        name="create_new_review"),
    url(r'^api/v0/review/list/$', ListReviews.as_view(),
        name="list_reviews"),
    url(r'^api/v0/review/(?P<option>update|delete|detail)/(?P<pk>[0-9]+)$',
        UpdateDestroyListReview.as_view(),
        name="update_destroy_and_detail_review"),
    # Notifications
    url(r'^api/v0/notification/list/$', ListNotification.as_view(),
        name="list_Notification"),
    url(r'^api/v0/notification/(?P<option>update|delete|detail)/(?P<pk>[0-9]+)$',
        UpdateDestroyListNotification.as_view(),
        name="update_destroy_and_detail_notification"),

]
