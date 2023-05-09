from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comments.models import Comment
from comments.serializers import CommentSerializer, CommentCreateSerializer
from posts.permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        author_id_str = self.request.query_params.get("author")
        post_id_str = self.request.query_params.get("post")
        queryset = super().get_queryset()

        if author_id_str:
            queryset = queryset.filter(author_id=int(author_id_str))

        if post_id_str:
            queryset = queryset.filter(post_id=int(post_id_str))

        return queryset

    def get_serializer_class(self):

        if self.action == "create":
            return CommentCreateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="author",
                type=int,
                description=(
                    "Filter by author id (ex. ?author_id=1)"
                )
            ),
            OpenApiParameter(
                name="post",
                type=int,
                description=(
                    "Filter by post id (ex. ?post_id=1)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
