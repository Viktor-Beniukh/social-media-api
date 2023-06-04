from typing import Any

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from posts.pagination import ApiPagination
from comments.models import Comment
from comments.serializers import CommentSerializer
from posts.models import Post


COMMENTS_URL = reverse("comments:comments-list")


def sample_comment(**params: dict) -> Comment:
    author = get_user_model().objects.create_user(
        email="author@test1.com",
        password="authortestpassword",
        username="AuthorTest1"
    )
    post = Post.objects.create(
        author=author,
        content="Post test"
    )

    defaults = {
        "author": author,
        "post": post,
        "comment_content": "This is a great post"
    }

    defaults.update(params)

    return Comment.objects.create(**defaults)


def detail_url(comment_id: int) -> Any:
    return reverse("comments:comments-detail", args=[comment_id])


class UnauthenticatedCommentApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_comments(self) -> None:
        sample_comment()

        response = self.client.get(COMMENTS_URL)

        comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_comment_detail(self) -> None:
        comment = sample_comment()
        url = detail_url(comment.id)

        response = self.client.get(url)

        serializer = CommentSerializer(comment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_comments_by_author_id(self):
        comment = sample_comment()
        pagination = ApiPagination

        response = self.client.get(COMMENTS_URL, {"author": f"{comment.author_id}"})

        serializer = CommentSerializer(pagination, comment)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)

    def test_filter_comments_by_post_id(self):
        comment = sample_comment()
        pagination = ApiPagination

        response = self.client.get(COMMENTS_URL, {"post": f"{comment.post_id}"})

        serializer = CommentSerializer(pagination, comment)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)
