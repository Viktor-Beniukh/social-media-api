from typing import Any

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from posts.pagination import ApiPagination
from posts.models import Post

from votes.models import Vote
from votes.serializers import VoteListSerializer, VoteDetailSerializer


VOTE_URL = reverse("votes:votes-list")


class UnauthenticatedVoteTestApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_votes(self) -> None:
        sample_vote()

        response = self.client.get(VOTE_URL)

        votes = Vote.objects.all()

        serializer = VoteListSerializer(votes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_vote_detail(self) -> None:
        vote = sample_vote()
        url = detail_url(vote.id)

        response = self.client.get(url)

        serializer = VoteDetailSerializer(vote)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_votes_by_post_id(self):
        votes = sample_vote()
        pagination = ApiPagination

        response = self.client.get(VOTE_URL, {"post": f"{votes.post_id}"})

        serializer = VoteListSerializer(pagination, votes)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)


def sample_vote(**params: dict) -> Vote:
    author = get_user_model().objects.create_user(
        email="author@test.com",
        password="authortestpassword",
        username="AuthorTest"
    )
    post = Post.objects.create(author=author)

    defaults = {
        "post": post,
    }

    defaults.update(params)

    return Vote.objects.create(**defaults)


def detail_url(vote_id: int) -> Any:
    return reverse("votes:votes-detail", args=[vote_id])
