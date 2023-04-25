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
