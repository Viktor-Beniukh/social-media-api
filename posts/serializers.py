from rest_framework import serializers

from comments.serializers import CommentSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
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
            "comments"
        )


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("author", "created_at", "hashtags")


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("id", "author", "created_at", "hashtags")
