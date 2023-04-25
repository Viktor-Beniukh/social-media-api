from rest_framework import viewsets, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user_profile.models import UserProfile
from user_profile.permissions import IsOwnerOrReadOnly
from user_profile.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        profile_instance = UserProfile.objects.filter(owner=self.request.user)

        if profile_instance.exists():
            raise serializers.ValidationError(
                {"message": "You have already your profile"}
            )
        serializer.save(owner=self.request.user)
