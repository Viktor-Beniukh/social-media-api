from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient

from api.views import ApiPagination
from posts.models import Post
from votes.models import Vote
from votes.serializers import VoteListSerializer


VOTE_URL = "http://127.0.0.1:8000/votes/"


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
