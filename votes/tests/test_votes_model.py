from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post
from votes.models import Vote


class ModelsTests(TestCase):

    def test_vote_str(self) -> None:
        author = get_user_model().objects.create_user(
            email="author@test.com",
            password="authortestpassword",
            username="AuthorTest"
        )
        post = Post.objects.create(
            author=author,
            content="Post test"
        )
        post_content = Vote.objects.create(
            post=post
        )
        self.assertEqual(str(post_content), post_content.post.content)
