from django.db.models import Count
from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from inspyre_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    API view for listing and creating posts.

    - GET: Retrieve a list of posts with optional filtering, searching, and
    ordering.
    - POST: Create a new post associated with the authenticated user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count("comment", distinct=True),
        likes_count=Count("likes", distinct=True),
    ).order_by("-created_at")

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        "owner__followed__owner__profile",
        "likes__owner__profile",
        "owner__profile",
        "owner__profile__profile_tags__name",
    ]
    search_fields = [
        "owner__username",
        "title",
        "content",
        "post_tags__name",
    ]
    ordering_fields = [
        "comments_count",
        "likes_count",
        "likes__created_at",
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific post.

    - GET: Retrieve a post by its ID.
    - PUT/PATCH: Update the post content or associated data if the user is
    the owner.
    - DELETE: Delete the post if the user is the owner.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count("comment", distinct=True),
        likes_count=Count("likes", distinct=True),
    ).order_by("-created_at")


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_posts(request):
    """
    Retrieve the top 10 most liked, approved posts.
    """
    trending = (
        Post.objects.filter(approval_status=0)
        .annotate(likes_count=Count("likes", distinct=True))
        .order_by("-likes_count")[:10]
    )
    serializer = PostSerializer(
        trending, many=True, context={"request": request}
    )
    return Response(serializer.data)
