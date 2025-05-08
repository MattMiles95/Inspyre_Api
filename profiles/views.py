from django.db.models import Count
from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from inspyre_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer, ProfileTagSerializer
from .models import ProfileTag
from followers.models import Follower
from followers.serializers import UserMiniSerializer


class ProfileTagListView(generics.ListAPIView):
    """
    API view for listing all profile tags.
    """
    queryset = ProfileTag.objects.all()
    serializer_class = ProfileTagSerializer


class ProfileList(generics.ListAPIView):
    """
    API view for listing all profiles.

    - GET: Retrieve all profiles with annotation for post, follower, and
    following counts.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
        followers_count=Count("owner__followed", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        "owner__following__followed__profile",
        "owner__followed__owner__profile",
    ]
    ordering_fields = [
        "posts_count",
        "followers_count",
        "following_count",
        "owner__following__created_at",
        "owner__followed__created_at",
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving or updating a profile if the user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
        followers_count=Count("owner__followed", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer


class UserDeleteView(APIView):
    """
    API view for deleting the authenticated user's account.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowersListView(generics.ListAPIView):
    """
    API view for listing the followers of a user by user ID.
    """
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        follower_ids = Follower.objects.filter(
            followed__id=user_id
        ).values_list(
            "owner", flat=True
        )
        return User.objects.filter(id__in=follower_ids)


class FollowingListView(generics.ListAPIView):
    """
    API view for listing the users that a user is following by user ID.
    """
    serializer_class = UserMiniSerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        following_ids = Follower.objects.filter(owner__id=user_id).values_list(
            "followed", flat=True
        )
        return User.objects.filter(id__in=following_ids)
