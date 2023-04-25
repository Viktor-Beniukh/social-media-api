from rest_framework import viewsets, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comments.models import Comment
from comments.serializers import CommentSerializer
from posts.permissions import IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author")
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        comment_instance = Comment.objects.filter(
            post__author=self.request.user
        )
        if comment_instance:
            raise serializers.ValidationError(
                {"message": "You can't comment your posts"}
            )
        serializer.save(author=self.request.user)
