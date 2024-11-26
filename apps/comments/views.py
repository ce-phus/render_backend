from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PostComment
from .serializers import (
    PostCommentSerializer, PostCommentCreateSerializer,
    
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow only the author to modify their comments
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCommentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostCommentCreateSerializer  # Use same serializer for updating content
        return PostCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        comment = self.get_object()
        if not comment.is_parent:
            return Response({'detail': 'This comment has no replies.'}, status=status.HTTP_400_BAD_REQUEST)
        replies = comment.children()
        serializer = PostCommentSerializer(replies, many=True)
        return Response(serializer.data)