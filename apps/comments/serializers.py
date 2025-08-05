from rest_framework import serializers
from .models import Comment
from apps.users.serializers import PublicUserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()
    thread_depth = serializers.ReadOnlyField(source='get_thread_depth')

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'post',
            'content',
            'parent',
            'created_at',
            'updated_at',
            'is_reply',
            'thread_depth',
            'replies_count'
        ]

        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def validate_content(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError(
                "Comment cannot be empty."
            )
        
        if len(value) > 280:
            raise serializers.ValidationError(
                "Comment too long. (max 280 characters)"
            )
        
        return value