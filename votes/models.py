from django.conf import settings
from django.db import models

from posts.models import Post


class Vote(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="votes"
    )
    up_vote_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="up_vote_user",
        blank=True,
        null=True,
        default=None
    )
    down_vote_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="down_vote_user",
        blank=True,
        null=True,
        default=None
    )

    def __str__(self):
        return self.post.content
