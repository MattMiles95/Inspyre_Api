from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class ProfileTag(models.Model):
    profile_tags_choices = [
        ("writer", "Writer"),
        ("artist", "Artist"),
        ("photographer", "Photographer"),
    ]
    name = models.CharField(
        max_length=50, choices=profile_tags_choices, unique=True
    )

    def __str__(self):
        return self.get_name_display()


class Profile(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    profile_tags = models.ManyToManyField(
        ProfileTag, blank=True, related_name="profiles"
    )
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="profile_images/", default="../ember_wv8ywv"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
