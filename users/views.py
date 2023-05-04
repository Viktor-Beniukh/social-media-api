from django.contrib.auth import logout
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status, generics, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from api.pagination import ApiPagination
from users.models import User, Relationship
from users.serializers import (
    UserSerializer,
    UserDetailSerializer,
    AuthTokenSerializer,
    RelationshipSerializer,
)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.select_related("profile_data")
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = ApiPagination

    def get_queryset(self):
        username = self.request.query_params.get("username")
        queryset = super().get_queryset()

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer

        if self.action in ("follow", "unfollow"):
            return RelationshipSerializer

        return super().get_serializer_class()

    @action(methods=["POST"], detail=True, url_path="follow")
    def follow(self, request, pk=None):
        user = self.get_object()
        follower = request.user
        if user == follower:
            return Response(
                {"error": "You cannot follow yourself"}
            )

        relationship, created = Relationship.objects.get_or_create(
            user=user, follower=follower
        )
        if not created:
            return Response(
                {"error": "You are already following this user"}
            )

        serializer = RelationshipSerializer(relationship)
        return Response(serializer.data)

    @action(methods=["POST"], detail=True, url_path="unfollow")
    def unfollow(self, request, pk=None):
        user = self.get_object()
        follower = request.user
        try:
            relationship = Relationship.objects.get(
                user=user, follower=follower
            )
        except Relationship.DoesNotExist:
            return Response(
                {"error": "You are not following this user"}
            )

        relationship.delete()
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                type=str,
                description=(
                    "Filter by username (ex. ?username=Admin)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserLogoutView(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response(
                {"message": "You logged out. Token revoked successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "You are not logged in."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
