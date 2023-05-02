from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient


from user_profile.models import UserProfile
from user_profile.serializers import ProfileSerializer


USERPROFILE_URL = "http://127.0.0.1:8000/profiles/"


def sample_userprofile(**params):
    owner = get_user_model().objects.create_user(
        email="author@test.com",
        password="authortestpassword",
        username="AuthorTest"
    )

    defaults = {
        "owner": owner
    }
    defaults.update(params)

    return UserProfile.objects.create(**defaults)


class UnauthenticatedUserProfilesApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_profiles(self) -> None:
        sample_userprofile()

        response = self.client.get(USERPROFILE_URL)

        profiles = UserProfile.objects.all()

        serializer = ProfileSerializer(profiles, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_user_profile_by_id(self):
        owner = sample_userprofile()

        response = self.client.get(USERPROFILE_URL, {"owner": f"{owner.id}"})

        user_profiles = UserProfile.objects.filter(owner_id=str(owner.id))
        serializer = ProfileSerializer(user_profiles, many=True)

        self.assertEqual(response.data, serializer.data)


class AuthenticatedUserProfileApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="author@test.com",
            password="authortestpassword",
            username="AuthorTest"
        )
        self.client.force_authenticate(self.user)

    def test_create_user_profile(self) -> None:

        payload = {
            "owner": self.user,
        }

        response = self.client.post(USERPROFILE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        profile = UserProfile.objects.get(id=response.data["id"])

        for key in payload:
            self.assertEqual(payload[key], getattr(profile, key))
