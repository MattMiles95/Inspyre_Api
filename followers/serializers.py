from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Follower


from django.contrib.auth.models import User
from rest_framework import serializers


class UserMiniSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for the User model, providing only the ID,
    username as 'owner', and profile image for quick references in follower
    lists.
    """
    owner = serializers.CharField(source="username")
    image = serializers.ImageField(source="profile.image")

    class Meta:
        model = User
        fields = ["id", "owner", "image"]


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model.

    Handles serialization of follower instances, including creating a new
    follower and providing read-only fields for owner and followed user
    information.
    """
    owner = serializers.ReadOnlyField(source="owner.username")
    followed_name = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = Follower
        fields = ["id", "owner", "created_at", "followed", "followed_name"]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "possible duplicate"
            })
