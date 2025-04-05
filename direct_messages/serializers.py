from rest_framework import serializers
from .models import Conversation, DirectMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - handles participant references"""
    class Meta:
        model = User
        fields = ['id', 'username']

class DirectMessageSerializer(serializers.ModelSerializer):
    """Serializer for DirectMessage model"""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    preview = serializers.ReadOnlyField()

    class Meta:
        model = DirectMessage
        fields = [
            'id',
            'sender',
            'receiver',
            'conversation',
            'content',
            'created_at',
            'updated_at',
            'read',
            'preview'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model"""
    participants = UserSerializer(many=True, read_only=True)
    messages = DirectMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'messages',
            'created_at'
        ]
