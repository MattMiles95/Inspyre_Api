from django.urls import path
from .views import MessageListAPIView, MessageDetailAPIView

urlpatterns = [
    path('messages/', MessageListAPIView.as_view()),
    path('messages/<int:message_id>/', MessageDetailAPIView.as_view()),
]