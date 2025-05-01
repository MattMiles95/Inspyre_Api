from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import DirectMessage, Conversation
from .serializers import DirectMessageSerializer, ConversationSerializer, UserSerializer


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class MessageListAPIView(ListCreateAPIView):
    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "read"]

    def get_queryset(self):
        conversation_id = self.request.GET.get("conversation_id")
        receiver_id = self.request.GET.get("receiver")

        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return DirectMessage.objects.none()

            if self.request.user not in conversation.participants.all():
                return DirectMessage.objects.none()

            return DirectMessage.objects.filter(
                conversation=conversation
            ).select_related("sender", "receiver")

        if receiver_id:
            try:
                receiver = User.objects.get(id=receiver_id)
            except User.DoesNotExist:
                return DirectMessage.objects.none()

            return DirectMessage.objects.filter(
                Q(sender=self.request.user, receiver=receiver)
                | Q(sender=receiver, receiver=self.request.user)
            ).select_related("sender", "receiver")

        return DirectMessage.objects.none()


class MessageDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            message = DirectMessage.objects.select_related("sender", "receiver").get(
                id=message_id
            )
            if message.sender != request.user and message.receiver != request.user:
                return Response(
                    {"error": "You don't have permission to view this message"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if message.receiver == request.user and not message.read:
                message.read = True
                message.save()

            serializer = DirectMessageSerializer(message)
            return Response(serializer.data)
        except DirectMessage.DoesNotExist:
            return Response(
                {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, message_id):
        try:
            message = DirectMessage.objects.get(id=message_id)
            if message.receiver != request.user:
                return Response(
                    {"error": "You don't have permission to mark this message as read"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            message.read = request.data.get("read", message.read)
            message.save()
            serializer = DirectMessageSerializer(message)
            return Response(serializer.data)
        except DirectMessage.DoesNotExist:
            return Response(
                {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, message_id):
        try:
            message = DirectMessage.objects.get(id=message_id)
            if message.sender != request.user:
                return Response(
                    {"error": "You don't have permission to delete this message"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DirectMessage.DoesNotExist:
            return Response(
                {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ConversationListAPIView(ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by(
            "-created_at"
        )


class ConversationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            if request.user not in conversation.participants.all():
                return Response(
                    {"error": "You don't have permission to view this conversation"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer = ConversationSerializer(
                conversation, context={"request": request}
            )
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            if request.user not in conversation.participants.all():
                return Response(
                    {"error": "You don't have permission to delete this conversation"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            conversation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["username"]

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(username__icontains=search)
        return queryset
