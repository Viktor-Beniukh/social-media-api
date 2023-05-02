from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Hashtag, Post


class ModelsTests(TestCase):

    def test_hashtag_str(self) -> None:
        hashtag = Hashtag.objects.create(
            name="#Django",
        )
        self.assertEqual(str(hashtag), hashtag.name)

    def test_post_str(self) -> None:
        author = get_user_model().objects.create_user(
            email="author@test.com",
            password="authortestpassword",
            username="AuthorTest"
        )
        content = Post.objects.create(
            author=author,
            content="Post test"
        )
        self.assertEqual(str(content), content.content)
