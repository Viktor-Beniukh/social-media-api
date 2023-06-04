from rest_framework import serializers

from user_profile.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = UserProfile
        fields = "__all__"
