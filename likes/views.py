from rest_framework import generics, permissions
from inspyre_api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    """
    API view for listing likes or creating a new like.

    - GET: Retrieve a list of likes.
    - POST: Create a new like if the user is authenticated.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    API view for retrieving or deleting a like by its ID.

    - GET: Retrieve a specific like.
    - DELETE: Delete the like if the user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
