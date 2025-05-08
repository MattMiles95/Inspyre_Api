from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from inspyre_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class ReportComment(APIView):
    """
    API view to handle reporting a comment. Updates the comment's approval
    status to 'reported'.

    Methods:
        put(self, request, pk): Updates the approval status of the specified
        comment to 'reported'.
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.approval_status = 1
            comment.save()
            return Response(
                {"status": "comment reported"},
                status=status.HTTP_200_OK
            )
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class CommentList(generics.ListCreateAPIView):
    """
    API view to list comments or create a new comment.

    - GET: Retrieve a list of comments filtered by post.
    - POST: Create a new comment for the authenticated user.
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["post"]

    def get_queryset(self):
        """
        Return a queryset of top-level comments (excluding replies).
        """
        return Comment.objects.filter(parent__isnull=True)

    def perform_create(self, serializer):
        """
        Save the new comment with the current user as the owner.
        """
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a comment.

    - GET: Retrieve a specific comment by ID.
    - PUT: Update the comment content if the user is the owner.
    - DELETE: Delete the comment if the user is the owner.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
