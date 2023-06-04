from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Relationship


USERS_URL = "http://127.0.0.1:8000/users/"


class ModelsTests(TestCase):

    def test_relationship_str(self) -> None:
        user = get_user_model().objects.create_user(
            email="author@test.com",
            password="authortestpassword",
            username="AuthorTest"
        )
        follower = get_user_model().objects.create_user(
            email="author@test1.com",
            password="authortestpassword1",
            username="AuthorTest1"
        )

        relationship = Relationship.objects.create(
            user=user,
            follower=follower
        )

        self.assertEqual(
            str(relationship),
            f"{relationship.user} is following {relationship.follower}"
        )
