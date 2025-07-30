from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Relationship, Profile
from .serializers import (
    UserSerializer,
    UserListSerializer,
    PublicUserSerializer,
    PasswordChangeSerializer,
    EmailVerificationTokenSerializer,
    ProfileSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ('retrieve',):
            return PublicUserSerializer
        if self.action == 'change_password':
            return PasswordChangeSerializer
        if self.action == 'verify_email':
            return EmailVerificationTokenSerializer
        return UserSerializer
    
    def get_permissions(self):
        # Registration and email verification: PUBLIC
        if self.action in ('create', 'verify_email'):
            return [permissions.AllowAny()]
        # User list: ADMIN ONLY
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        # Details and edit: JUST THE USER
        if self.action in ('retrieve', 'update', 'partial_update', 'change_password'):
            return [permissions.IsAuthenticated()]
        # Destroy: ADMIN ONLY
        if self.action == 'destroy':
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], url_path='change-password')
    def change_password(self, request, pk=None):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        return Response({'detail': 'Password updated succesfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated()])
    def me(self, request):
        serializer = PublicUserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated()])
    def follow(self, request):
        target = self.get_object()
        if Relationship.objects.filter(from_user=request.user, to_user=target).exists():
            return Response({'detail': 'Already following.'}, status=status.HTTP_400_BAD_REQUEST)
        Relationship.objects.create(from_user=request.user, to_user=target)
        return Response({'detail': 'Now following.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated()])
    def unfollow(self, request, pk=None):
        target = self.get_object()
        rel = Relationship.objects.filter(from_user=request.user, to_user=target).first()
        if not rel:
            return Response({'detail': 'Not Following.'}, status=status.HTTP_400_BAD_REQUEST)
        rel.delete()
        return Response({'detail': 'Unfollowed.'}, status=status.HTTP_200_OK)
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated()]

    def get_object(self):
        # Always return the user's profile if auth
        return Profile.objects.get(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        # Not every profile; redirects to me details
        return self.retrieve(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)