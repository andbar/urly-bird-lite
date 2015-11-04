from django.conf.urls import include, url
from api.views import BookmarkListView, BookmarkDetailView, UserListView, UserDetailView, ClickListView, ClickDetailView

urlpatterns = [
    url(r'^bookmark/$', BookmarkListView.as_view(), name="api_bookmark_list"),
    url(r'^bookmark/(?P<pk>\d+)/$', BookmarkDetailView.as_view(), name="api_bookmark_detail"),
    url(r'^user/$', UserListView.as_view(), name="api_user_list"),
    url(r'^user/(?P<pk>\d+)/$', UserDetailView.as_view(), name="api_user_detail"),
    url(r'^click/$', ClickListView.as_view(), name="api_click_list"),
    url(r'^click/(?P<pk>\d+)/$', ClickDetailView.as_view(), name="api_click_detail"),
]