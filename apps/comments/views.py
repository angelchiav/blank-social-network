from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.response import Response

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        try:
            post_id = self.request.query_params.get('post')
            post_id = int(post_id)
            if post_id:
                return Comment.objects.filter(post_id=post_id).order_by('-created_at')
            return Comment.objects.all()
        
        except (TypeError, ValueError):
            return Comment.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def report(self, request, pk=None):
        comment = self.get_object()
        return Response({'status': 'comment reported'})