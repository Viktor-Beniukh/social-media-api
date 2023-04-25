from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
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
            "hashtags"
        )


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("author", "created_at", "hashtags")


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("id", "author", "created_at", "hashtags")
