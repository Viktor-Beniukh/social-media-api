from django.shortcuts import get_object_or_404
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
    permission_classes = (IsAuthenticatedOrReadOnly, HasSelfVotedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return VoteListSerializer

        if self.action == "retrieve":
            return VoteDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        post_instance = get_object_or_404(Post, pk=self.request.data["post"])

        if post_instance.author == self.request.user:
            raise serializers.ValidationError(
                {"message": "You can’t evaluate your own posts"}
            )

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
