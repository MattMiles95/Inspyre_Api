from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

APPROVAL_STATUS = ((0, "Approved"), (1, "Reported"))


class PostTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Post model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="images/",
        blank=True,
    )
    post_tags = models.ManyToManyField(PostTag, blank=True, related_name="posts")
    approval_status = models.IntegerField(choices=APPROVAL_STATUS, default=0)
    original_author = models.BooleanField(
        default=False,
        help_text="Check this box if you are the original creator of this content.",
    )

    def get_thumbnail_url(self):
        """Returns URL for thumbnail display"""
        if self.image:
            return self.image.url
        elif self.content:
            truncated_content = Truncator(self.content).words(50)
            return f"/content-preview/{truncated_content}"
        return None

    @property
    def thumbnail(self):
        """Property to handle thumbnail display logic"""
        url = self.get_thumbnail_url()
        if url.startswith("/content-preview/"):
            return {"type": "content", "preview": url.split("/")[-1]}
        return {"type": "image", "url": url}

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} {self.title}"
