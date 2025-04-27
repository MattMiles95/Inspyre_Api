from rest_framework import serializers
from .models import Conversation, DirectMessage
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - handles participant references"""

    profile_image = serializers.ImageField(source="profile.image", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "profile_image"]


class DirectMessageSerializer(serializers.ModelSerializer):
    """Serializer for DirectMessage model"""

    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    preview = serializers.ReadOnlyField()

    class Meta:
        model = DirectMessage
        fields = [
            "id",
            "sender",
            "receiver",
            "conversation",
            "content",
            "created_at",
            "updated_at",
            "read",
            "preview",
        ]
        extra_kwargs = {
            "conversation": {"read_only": True},
        }

    def create(self, validated_data):
        sender = self.context["request"].user
        receiver = validated_data["receiver"]

        conversation = (
            Conversation.objects.filter(participants=sender)
            .filter(participants=receiver)
            .first()
        )

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.set([sender, receiver])
            conversation.save()

        message = DirectMessage.objects.create(
            sender=sender,
            receiver=receiver,
            conversation=conversation,
            content=validated_data["content"],
        )
        return message


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "messages",
            "latest_message",
            "created_at",
        ]

    def get_latest_message(self, obj):
        latest = obj.messages.order_by("-created_at").first()
        if latest:
            return DirectMessageSerializer(latest).data
        return None
