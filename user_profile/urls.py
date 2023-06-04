from rest_framework import routers

from user_profile.views import ProfileViewSet


app_name = "user_profile"


router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = router.urls
