import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from posts.models import Post


def comment_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = (
        f"{slugify(instance.author.username)}-{slugify(instance.post_id)}"
        f"-{uuid.uuid4()}{extension}"
    )

    return os.path.join("uploads/comments/", filename)


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    comment_content = models.CharField(max_length=500, blank=True)
    comment_date = models.DateField(auto_now_add=True)
    comment_image = models.ImageField(
        upload_to=comment_image_file_path, blank=True
    )
