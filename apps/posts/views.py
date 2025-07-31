from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer, PostListSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def perfom_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset