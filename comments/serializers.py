from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = (
            "id",
            "comment_content",
            "comment_image",
            "comment_date",
            "commented_by",
            "post",
        )


class CommentCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(CommentCreateSerializer, self).validate(attrs=attrs)

        if attrs["post"].author.email == attrs["author"].email:
            raise serializers.ValidationError(
                {"message": "You can't comment your posts"}
            )

        return data

    class Meta:
        model = Comment
        fields = ("comment_content", "comment_image", "post", "author",)
