"""urly_bird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from urly_app.views import BookmarkList, UserBookmarkList, BookmarkCreate, ClickShortcut, UserIndex, BookmarkDelete, \
    BookmarkDetail, BookmarkUpdate, UserCreate

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', BookmarkList.as_view(), name="bookmark_list"),
    url(r'^user/(?P<pk>\d+)/$', UserBookmarkList.as_view(), name="user_bookmark_list"),
    url(r'^createbookmark/$', login_required(BookmarkCreate.as_view()), name="bookmark_create"),
    url(r'^c/(?P<bookmark_shortcut>.+)/$', ClickShortcut.as_view(), name="click_shortcut"),
    url(r'^index/$', UserIndex.as_view(), name="user_index"),
    url(r'^delete/(?P<bookmark_id>\d+)/$', login_required(BookmarkDelete.as_view()), name="delete_bookmark"),
    url(r'^(?P<pk>\d+)/$', BookmarkDetail.as_view(), name="bookmark_detail"),
    url(r'^updatebookmark/(?P<pk>\d+)/$', login_required(BookmarkUpdate.as_view()), name="update_bookmark"),
    url(r'^createuser/$', UserCreate.as_view(), name="create_user"),
    url(r'^api/', include('api.urls')),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
