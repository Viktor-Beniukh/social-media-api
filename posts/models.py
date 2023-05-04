import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = (
        f"{slugify(instance.author.username)}-{slugify(instance.created_at)}"
        f"-{uuid.uuid4()}{extension}"
    )

    return os.path.join("uploads/posts/", filename)


class Hashtag(models.Model):
    name = models.CharField(
        max_length=255, unique=True, blank=True, default=None
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(
        upload_to=post_image_file_path, blank=True
    )
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.content
