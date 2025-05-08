from rest_framework import serializers
from .models import Conversation, DirectMessage
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, including profile image for participant
    references. Provides a simplified representation of the user in
    conversation and direct message contexts.
    """

    profile_image = serializers.ImageField(
        source="profile.image", read_only=True
        )

    class Meta:
        model = User
        fields = ["id", "username", "profile_image"]


class DirectMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the DirectMessage model, providing sender and receiver
    details, as well as a preview of the message content.

    Includes nested UserSerializer for sender and receiver and a read-only
    preview field.
    """

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
        """
        Create a new direct message between the sender and receiver.
        Automatically associates the message with an existing or new
        conversation.
        """
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
    """
    Serializer for the Conversation model, providing participant details,
    the latest message, whether there are any unread messages,and a
    reference to the other user in the conversation.

    Includes nested UserSerializer for participants and the latest message.
    """
    participants = UserSerializer(many=True, read_only=True)
    latest_message = serializers.SerializerMethodField()
    other_user = serializers.SerializerMethodField()
    has_unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "messages",
            "latest_message",
            "created_at",
            "other_user",
            "has_unread_messages",
        ]

    def get_latest_message(self, obj):
        latest = obj.messages.order_by("-created_at").first()
        return DirectMessageSerializer(latest).data if latest else None

    def get_other_user(self, obj):
        request = self.context.get("request")
        user = request.user
        other_user = obj.participants.exclude(id=user.id).first()
        return UserSerializer(other_user).data if other_user else None

    def get_has_unread_messages(self, obj):
        """
        Check if the user has any unread messages in this conversation.
        """
        user = self.context["request"].user
        return obj.messages.filter(receiver=user, read=False).exists()
