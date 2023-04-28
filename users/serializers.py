from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers

from user_profile.serializers import ProfileSerializer
from users.models import Relationship


class RelationshipSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    user = serializers.ReadOnlyField()

    class Meta:
        model = Relationship
        fields = "__all__"


class FollowingSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(
        source="follower.username", read_only=True
    )

    class Meta:
        model = Relationship
        fields = ("follower", )


class FollowersSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source="user.username", read_only=True
    )

    class Meta:
        model = Relationship
        fields = ("user", )


class UserSerializer(serializers.ModelSerializer):
    profile_data = ProfileSerializer(read_only=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "profile_data",
            "following",
            "followers",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

    @staticmethod
    def get_following(obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    @staticmethod
    def get_followers(obj):
        return FollowersSerializer(obj.followers.all(), many=True).data


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"),
                                email=email, password=password)

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("Must include 'email' and 'password'.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs
