import hashlib
import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, View, DetailView, UpdateView
from urly_app.models import Bookmark, Click


class BookmarkList(ListView):
    model = Bookmark


class BookmarkDetail(DetailView):
    model = Bookmark


class UserBookmarkList(ListView):
    model = Bookmark

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return self.model.objects.filter(creator__id=user_id)


class UserCreate(CreateView):
    model = User
    success_url = "/"
    form_class = UserCreationForm


class BookmarkCreate(CreateView):
    model = Bookmark
    fields = ["title", "full_link", "description"]
    success_url = "/"

    def form_valid(self, form):
        model = form.save(commit=False)
        model.creator = self.request.user
        full_link = form.instance.full_link + str(model.creator.id)
        model.shortcut = hashlib.md5(full_link.encode('utf-8')).hexdigest()[:random.randint(5, 20)]
        return super().form_valid(form)


class BookmarkUpdate(UpdateView):
    model = Bookmark
    fields = ["title", "description"]
    success_url = "/"


class BookmarkDelete(View):

    def post(self, request, bookmark_id):
        Bookmark.objects.get(id=bookmark_id).delete()
        return HttpResponseRedirect(reverse("user_bookmark_list", kwargs={'pk':request.user.id}))


class UserIndex(View):

    def get(self, request):
        user = request.user.id
        return HttpResponseRedirect(reverse("user_bookmark_list", kwargs={'pk':user}))


class ClickShortcut(View):

    def get(self, request, bookmark_shortcut):
        bookmark = Bookmark.objects.get(shortcut=bookmark_shortcut)
        return HttpResponseRedirect(bookmark.full_link)

    def post(self, request, bookmark_shortcut):
        bookmark = Bookmark.objects.get(shortcut=bookmark_shortcut)
        if request.user.id:
            Click.objects.create(clicker=request.user, bookmark=bookmark)
        else:
            Click.objects.create(bookmark=bookmark)
        return HttpResponseRedirect(bookmark.full_link)