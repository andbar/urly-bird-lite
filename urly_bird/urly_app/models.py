from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Bookmark(models.Model):
    creator = models.ForeignKey(User)
    shortcut = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    full_link = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    @property
    def num_clicks(self):
        clicks = Click.objects.filter(bookmark=self)
        return clicks.count()

    def __str__(self):
        return self.title


class Click(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    clicker = models.ForeignKey(User, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.clicker