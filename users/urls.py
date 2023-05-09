from django.urls import path
from rest_framework import routers

from users.views import (
    UserViewSet,
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    UserLogoutView
)


app_name = "users"


router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("users/register/", CreateUserView.as_view(), name="create"),
    path("users/token/", CreateTokenView.as_view(), name="token"),
    path("users/me/", ManageUserView.as_view(), name="manage"),
    path("users/logout/", UserLogoutView.as_view(), name="logout"),
]

urlpatterns += router.urls
