from rest_framework import serializers

from comments.serializers import CommentSerializer
from posts.models import Post, Hashtag
from votes.serializers import VoteListSerializer


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    votes = VoteListSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    hashtags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "post_image",
            "hashtags",
            "comments",
            "votes"
        )


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("author", "created_at")


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("id", "author", "created_at")


class CreateHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name")
