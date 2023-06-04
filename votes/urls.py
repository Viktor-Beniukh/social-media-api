from rest_framework import routers

from votes.views import VoteViewSet

app_name = "votes"


router = routers.DefaultRouter()
router.register("votes", VoteViewSet, basename="votes")


urlpatterns = router.urls
