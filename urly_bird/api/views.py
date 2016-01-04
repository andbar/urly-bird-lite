from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here
from rest_framework.fields import ReadOnlyField
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from urly_app.models import Bookmark, Click
from rest_framework import permissions


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class BookmarkSerializer(ModelSerializer):
    creator = ReadOnlyField(source='creator.username')
    num_clicks = ReadOnlyField()

    class Meta:
        model = Bookmark


class ClickSerializer(ModelSerializer):
    clicker = ReadOnlyField(source='clicker.username')

    class Meta:
        model = Click


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.creator == request.user


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookmarkListView(ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BookmarkDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class ClickListView(ListCreateAPIView):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(clicker=self.request.user)
        else:
            serializer.save(clicker=None)


class ClickDetailView(RetrieveAPIView):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer