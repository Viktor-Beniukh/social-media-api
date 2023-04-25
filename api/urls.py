from django.urls import path
from rest_framework import routers

from user_profile.views import ProfileViewSet
from users.views import (
    UserViewSet,
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    UserLogoutView
)

app_name = "api"

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
    path("users/register/", CreateUserView.as_view(), name="create"),
    path("users/token/", CreateTokenView.as_view(), name="token"),
    path("users/me/", ManageUserView.as_view(), name="manage"),
    path("users/logout/", UserLogoutView.as_view(), name="logout")
]

urlpatterns += router.urls
