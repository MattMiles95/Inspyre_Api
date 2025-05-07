from rest_framework import serializers
from .models import Conversation, DirectMessage
from django.contrib.auth.models import User
import logging


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - handles participant references"""

    profile_image = serializers.ImageField(
        source="profile.image", read_only=True
    )

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
        receiver_id = self.context["request"].data.get("receiver")

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver not found.")

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
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "messages",
            "latest_message",
            "created_at",
            "other_user",
        ]

    def get_latest_message(self, obj):
        try:
            latest = DirectMessage.objects.filter(
                conversation=obj
            ).order_by("-created_at").first()

            logging.info(f"Latest message for {obj.id}: {latest}")

            if latest:
                return {
                    "id": latest.id,
                    "content": latest.content,
                    "created_at": latest.created_at,
                    "sender": latest.sender.username,
                }
        except DirectMessage.DoesNotExist:
            logging.warning(f"No messages found for conversation {obj.id}")
            return None
        return None

    def get_other_user(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        user = request.user
        other = obj.participants.exclude(id=user.id).first()
        return UserSerializer(other).data if other else None
