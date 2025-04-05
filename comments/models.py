from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

APPROVAL_STATUS = ((0, "Approved"), (1, "Reported"))


class Comment(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    approval_status = models.IntegerField(choices=((0, "Approved"), (1, "Reported")), default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content