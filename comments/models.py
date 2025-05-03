from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

APPROVAL_STATUS = ((0, "Approved"), (1, "Reported"))


class Comment(models.Model):
    """
    Comment model, related to User and Post
    Can optionally be a reply to another comment via 'parent'.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    approval_status = models.IntegerField(choices=APPROVAL_STATUS, default=0)

    class Meta:
        ordering = ["parent__id", "-created_at"]

    def __str__(self):
        return self.content
