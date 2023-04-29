from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user_profile.models import UserProfile
from user_profile.permissions import IsOwnerOrReadOnly
from user_profile.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related("owner")
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        owner_id_str = self.request.query_params.get("owner")
        queryset = self.queryset

        if owner_id_str:
            queryset = queryset.filter(owner_id=int(owner_id_str))

        return queryset

    def perform_create(self, serializer):
        profile_instance = UserProfile.objects.filter(owner=self.request.user)

        if profile_instance.exists():
            raise serializers.ValidationError(
                {"message": "You have already your profile"}
            )
        serializer.save(owner=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="owner",
                type=int,
                description=(
                    "Filter by owner id (ex. ?owner_id=1)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
