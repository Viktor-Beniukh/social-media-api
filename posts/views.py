from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.response import Response

from api.pagination import ApiPagination
from posts.models import Post
from posts.serializers import (
    PostSerializer,
    CreatePostSerializer,
    UpdatePostSerializer,
    CreateHashtagSerializer
)
from posts.permissions import IsAuthorOrReadOnly
from posts.tasks import create_post


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects
        .select_related("author")
        .prefetch_related("hashtags")
    )
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = ApiPagination

    def get_queryset(self):
        author_id_str = self.request.query_params.get("author")
        hashtags = self.request.query_params.get("hashtags")
        queryset = super().get_queryset()

        if author_id_str:
            queryset = queryset.filter(author_id=author_id_str)

        if hashtags:
            queryset = queryset.filter(hashtags__name__icontains=hashtags)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePostSerializer

        if self.action == "update":
            return UpdatePostSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user)

            scheduled_at = serializer.validated_data.get("scheduled_at")
            if scheduled_at and scheduled_at > timezone.now():
                create_post.apply_async(args=[serializer.validated_data])
                return Response(
                    serializer.data, status=status.HTTP_202_ACCEPTED
                )

        self.perform_create(serializer)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtags",
                type=str,
                description=(
                    "Filter by hashtags (ex. ?hashtags=#Django)"
                )
            ),
            OpenApiParameter(
                name="author",
                type=int,
                description=(
                    "Filter by author id (ex. ?author_id=1)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CreateHashtagView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateHashtagSerializer
