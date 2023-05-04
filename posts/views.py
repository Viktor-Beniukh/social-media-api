from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
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
    UpdatePostSerializer, CreateHashtagSerializer
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
        queryset = self.queryset

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

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["POST"], detail=False)
    def schedule_post(self, request):
        author_id = request.data["author_id"]
        content = request.data["content"]
        created_at = request.data["created_at"]
        post_image = request.data.get("post_image", None)
        hashtags = request.data.get("hashtags", None)

        scheduled_time = timezone.now()

        create_post.apply_async(
            args=[author_id, content, created_at, post_image, hashtags],
            eta=scheduled_time
        )

        return Response(
            {
                "scheduled_time": scheduled_time,
                "message": "Post scheduled Successfully"
            }
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
