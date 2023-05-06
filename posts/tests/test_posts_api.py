from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from api.pagination import ApiPagination
from posts.models import Post, Hashtag
from posts.serializers import PostSerializer


POST_URL = "http://127.0.0.1:8000/posts/"
HASHTAG_URL = "http://127.0.0.1:8000/posts/hashtags/"


def sample_post(**params: dict) -> Post:
    author = get_user_model().objects.create_user(
        email="author@test1.com",
        password="authortestpassword",
        username="AuthorTest1"
    )

    defaults = {
        "author": author,
        "content": "Test post",
    }

    defaults.update(params)

    return Post.objects.create(**defaults)


class UnauthenticatedPostApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_posts(self) -> None:
        sample_post()
        pagination = ApiPagination

        response = self.client.get(POST_URL)

        posts = Post.objects.all()

        serializer = PostSerializer(pagination, posts, many=True)

        if serializer.is_valid():
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_filter_posts_by_hashtag(self):
        author1 = get_user_model().objects.create_user(
            email="author1@test1.com",
            password="authortestpassword1",
            username="AuthorTest2"
        )
        author2 = get_user_model().objects.create_user(
            email="author2@test2.com",
            password="authortestpassword2",
            username="UserTest2"
        )
        post1 = Post.objects.create(author=author1)
        post2 = Post.objects.create(author=author2)
        post3 = sample_post()

        hashtag1 = Hashtag.objects.create(name="#Django")
        hashtag2 = Hashtag.objects.create(name="#Python")

        post1.hashtags.add(hashtag1)
        post2.hashtags.add(hashtag2)

        pagination = ApiPagination

        response = self.client.get(POST_URL, {"hashtags": f"{hashtag1.name}"})

        serializer1 = PostSerializer(pagination, post1)
        serializer2 = PostSerializer(pagination, post2)
        serializer3 = PostSerializer(pagination, post3)

        if serializer1.is_valid():
            self.assertIn(serializer1.data, response.data)

        if serializer2.is_valid():
            self.assertIn(serializer2.data, response.data)

        if serializer3.is_valid():
            self.assertNotIn(serializer3.data, response.data)

    def test_filter_post_by_author_id(self):
        post = sample_post()
        pagination = ApiPagination

        response = self.client.get(POST_URL, {"author": f"{post.author_id}"})

        serializer = PostSerializer(pagination, post)

        if serializer.is_valid():
            self.assertEqual(response.data, serializer.data)


class AuthenticatedPostApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="author@test.com",
            password="authortestpassword",
            username="AuthorTest"
        )
        self.client.force_authenticate(self.user)

    def test_create_post(self) -> None:

        payload = {
            "author": self.user,
            "content": "Test post"
        }

        response = self.client.post(POST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(content=response.data["content"])

        for key in payload:
            self.assertEqual(payload[key], getattr(post, key))


class AuthenticatedHashtagsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="author@test.com",
            password="authortestpassword",
            username="AuthorTest"
        )
        self.client.force_authenticate(self.user)

    def test_create_post(self) -> None:

        payload = {
            "name": "#Python"
        }

        response = self.client.post(HASHTAG_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        hashtag = Hashtag.objects.get(name=response.data["name"])

        for key in payload:
            self.assertEqual(payload[key], getattr(hashtag, key))
