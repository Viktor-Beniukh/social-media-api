from django.contrib.auth import get_user_model
from django.test import TestCase

from comments.models import Comment
from posts.models import Post


class ModelsTests(TestCase):

    def test_comment_str(self) -> None:

        author = get_user_model().objects.create_user(
            email="author@test.com",
            password="authortestpassword",
            username="AuthorTest"
        )
        post = Post.objects.create(
            author=author,
            content="Post test"
        )
        comment = Comment.objects.create(
            author=author,
            post=post,
            comment_content="This is a great post"
        )
        self.assertEqual(str(comment), comment.comment_content)
