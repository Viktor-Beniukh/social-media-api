from django.urls import path
from rest_framework import routers

from posts.views import PostViewSet, CreateHashtagView

app_name = "posts"


router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path(
        "posts/hashtags/",
        CreateHashtagView.as_view(),
        name="hashtag-create"
    )
]

urlpatterns += router.urls
