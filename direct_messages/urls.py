from django.urls import path
from .views import (
    MessageListAPIView,
    MessageDetailAPIView,
    ConversationListAPIView,
    ConversationDetailAPIView,
    UserListAPIView,
)

urlpatterns = [
    path("messages/", MessageListAPIView.as_view()),
    path("messages/<int:message_id>/", MessageDetailAPIView.as_view()),
    path("conversations/", ConversationListAPIView.as_view()),
    path("conversations/<int:conversation_id>/", ConversationDetailAPIView.as_view()),
    path("users/", UserListAPIView.as_view()),
]
