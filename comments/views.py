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
    List comments or create a comment if logged in.
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["post"]

    def get_queryset(self):
        return Comment.objects.filter(parent__isnull=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, or update or delete it by id if you own it.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
