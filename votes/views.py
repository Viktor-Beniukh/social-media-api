from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Post
from votes.models import Vote
from votes.permissions import HasSelfVotedOrReadOnly
from votes.serializers import (
    VoteSerializer,
    VoteListSerializer,
    VoteDetailSerializer
)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.select_related(
        "post", "up_vote_by", "down_vote_by"
    )
    serializer_class = VoteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        HasSelfVotedOrReadOnly,
    )

    def get_queryset(self):
        post_id_str = self.request.query_params.get("post")
        queryset = super().get_queryset()

        if post_id_str:
            queryset = queryset.filter(post_id=int(post_id_str))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return VoteListSerializer

        if self.action == "retrieve":
            return VoteDetailSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        post_instance = get_object_or_404(Post, pk=self.request.data["post"])

        if self.request.data["up_vote_by"]:
            already_up_voted = Vote.objects.filter(
                post=post_instance, up_vote_by=self.request.user
            ).exists()
            if already_up_voted:
                raise serializers.ValidationError(
                    {"message": "You have already liked this post"}
                )
            else:
                serializer.save(
                    up_vote_by=self.request.user, post=post_instance
                )

        else:
            already_down_voted = Vote.objects.filter(
                post=post_instance, down_vote_by=self.request.user
            ).exists()
            if already_down_voted:
                raise serializers.ValidationError(
                    {"message": "You have already disliked this post"}
                )
            else:
                serializer.save(
                    down_vote_by=self.request.user, post=post_instance
                )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="post",
                type=int,
                description=(
                    "Filter by post id (ex. ?post_id=1)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
