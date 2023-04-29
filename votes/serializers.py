from rest_framework import serializers

from votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ("id", "post", "up_vote_by", "down_vote_by")


class VoteListSerializer(VoteSerializer):
    up_vote_by = serializers.ReadOnlyField(
        source="up_vote_by.username"
    )
    down_vote_by = serializers.ReadOnlyField(
        source="down_vote_by.username"
    )


class VoteDetailSerializer(serializers.ModelSerializer):
    up_vote_by_username = serializers.ReadOnlyField(
        source="up_vote_by.username"
    )
    down_vote_by_username = serializers.ReadOnlyField(
        source="down_vote_by.username"
    )

    class Meta:
        model = Vote
        fields = (
            "id",
            "post",
            "up_vote_by",
            "up_vote_by_username",
            "down_vote_by",
            "down_vote_by_username"
        )
