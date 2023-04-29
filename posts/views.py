from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.views import ApiPagination
from posts.models import Post
from posts.serializers import (
    PostSerializer,
    CreatePostSerializer,
    UpdatePostSerializer
)
from posts.permissions import IsAuthorOrReadOnly


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
        hashtags = self.request.query_params.get("hashtags")
        queryset = self.queryset

        if hashtags:
            queryset = queryset.filter(hashtags__name__in=hashtags)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePostSerializer

        if self.action == "update":
            return UpdatePostSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
