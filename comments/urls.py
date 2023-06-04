from rest_framework import routers

from comments.views import CommentViewSet

app_name = "comments"


router = routers.DefaultRouter()
router.register("comments", CommentViewSet, basename="comments")


urlpatterns = router.urls
