from django.urls import path, include
from rest_framework import routers

from comments.views import CommentViewSet
from posts.views import PostViewSet
from user_profile.views import ProfileViewSet
from users.views import (
    UserViewSet,
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    UserLogoutView,
)
from votes.views import VoteViewSet


app_name = "api"


router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")
router.register("votes", VoteViewSet, basename="votes")


urlpatterns = [
    path("", include(router.urls)),
    path("users/register/", CreateUserView.as_view(), name="create"),
    path("users/token/", CreateTokenView.as_view(), name="token"),
    path("users/me/", ManageUserView.as_view(), name="manage"),
    path("users/logout/", UserLogoutView.as_view(), name="logout"),
]
