from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import DirectMessage
from .serializers import DirectMessageSerializer

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MessageListAPIView(ListCreateAPIView):
    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'read']

    def get_queryset(self):
        receiver_id = self.request.GET.get('receiver')
        if not receiver_id:
            return DirectMessage.objects.none()
            
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return DirectMessage.objects.none()
            
        return DirectMessage.objects.filter(
            Q(sender=self.request.user, receiver=receiver) |
            Q(sender=receiver, receiver=self.request.user)
        ).select_related('sender', 'receiver')

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver not found")
        serializer.save(sender=self.request.user, receiver=receiver)

class MessageDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            message = DirectMessage.objects.select_related('sender', 'receiver').get(id=message_id)
            if message.sender != request.user and message.receiver != request.user:
                return Response(
                    {"error": "You don't have permission to view this message"},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = DirectMessageSerializer(message)
            return Response(serializer.data)
        except DirectMessage.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, message_id):
        try:
            message = DirectMessage.objects.get(id=message_id)
            if message.receiver != request.user:
                return Response(
                    {"error": "You don't have permission to mark this message as read"},
                    status=status.HTTP_403_FORBIDDEN
                )
            message.read = request.data.get('read', message.read)
            message.save()
            serializer = DirectMessageSerializer(message)
            return Response(serializer.data)
        except DirectMessage.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)