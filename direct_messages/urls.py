from django.urls import path
from .views import (
    MessageListAPIView,
    MessageDetailAPIView,
    ConversationListAPIView,
    ConversationDetailAPIView,
    UserListAPIView,
)

urlpatterns = [
    path("messages/", MessageListAPIView.as_view(), name="message-list"),
    path(
        "messages/<int:message_id>/",
        MessageDetailAPIView.as_view(),
        name="message-detail",
    ),
    path(
        "conversations/",
        ConversationListAPIView.as_view(),
        name="conversation-list"),
    path(
        "conversations/<int:conversation_id>/",
        ConversationDetailAPIView.as_view(),
        name="conversation-detail",
    ),
    path("users/", UserListAPIView.as_view(), name="user-list"),
]
