from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {', '.join([user.username for user in self.participants.all()])}"


class DirectMessage(models.Model):
    """
    Model representing a private message between two users within a conversation thread.
    Similar to comments but restricted to private viewing.
    """

    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.SET_NULL, null=True
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.SET_NULL, null=True
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        truncated_content = Truncator(self.content).words(20)
        return f"Message from {self.sender} to {self.receiver}: {truncated_content}"

    @property
    def preview(self):
        """Return a short preview of the message content."""
        return Truncator(self.content).words(10)
