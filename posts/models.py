from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

APPROVAL_STATUS = ((0, "Approved"), (1, "Reported"))


class PostTag(models.Model):
    """
    Model representing a tag that can be associated with a post.

    Attributes:
        name (str): The name of the tag (unique).
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model representing a post created by a user, which can include content,
    an image, and associated tags. Supports approval status for moderation.

    Attributes:
        owner (User): The user who created the post.
        created_at (datetime): The timestamp of when the post was created.
        updated_at (datetime): The timestamp of the last update to the post.
        title (str): The title of the post.
        content (str): The text content of the post.
        image (ImageField): An optional image associated with the post.
        post_tags (ManyToManyField): Tags associated with the post.
        approval_status (int): Approval status, 0 for approved, 1 for
        reported.
        original_author (bool): Flag indicating if the user is the original
        author.
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
    post_tags = models.ManyToManyField(
        PostTag, blank=True, related_name="posts"
    )
    approval_status = models.IntegerField(choices=APPROVAL_STATUS, default=0)
    original_author = models.BooleanField(
        default=False,
        help_text="Check this box if you are the original creator of this "
        "content.",
    )

    def get_thumbnail_url(self):
        """
        Returns a URL for the post thumbnail.
        If an image is available, its URL is returned.
        If content is present but no image, a truncated content preview URL
        is returned.
        """
        if self.image:
            return self.image.url
        elif self.content:
            truncated_content = Truncator(self.content).words(50)
            return f"/content-preview/{truncated_content}"
        return None

    @property
    def thumbnail(self):
        """
        Property to handle thumbnail display logic, returning a dictionary
        with 'type' (image or content) and 'url' or 'preview'.
        """
        url = self.get_thumbnail_url()
        if url.startswith("/content-preview/"):
            return {"type": "content", "preview": url.split("/")[-1]}
        return {"type": "image", "url": url}

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} {self.title}"
