from typing import Any

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from posts.pagination import ApiPagination
from users.models import User
from users.serializers import UserSerializer


USERS_URL = reverse("users:users-list")


class UnauthenticatedUsersApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_users(self) -> None:
        sample_user()
        pagination = ApiPagination

        response = self.client.get(USERS_URL)

        user = User.objects.all()

        serializer = UserSerializer(pagination, user, many=True)

        if serializer.is_valid():
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_retrieve_user_detail(self) -> None:
        user = sample_user()
        url = detail_url(user.id)

        response = self.client.get(url)

        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_users_by_username(self):
        sample_user(username="AuthorTest")
        sample_user(email="author@test1.com", username="UserTest")
        pagination = ApiPagination

        response = self.client.get(USERS_URL, {"username": "AuthorTest"})

        users = User.objects.filter(username__icontains="author")
        serializer = UserSerializer(pagination, users, many=True)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)


def sample_user(**params):

    defaults = {
        "email": "author@test.com",
        "password": "authortestpassword",
        "username": "AuthorTest"
    }
    defaults.update(params)

    return User.objects.create(**defaults)


def detail_url(user_id: int) -> Any:
    return reverse("users:users-detail", args=[user_id])
