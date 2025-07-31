from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username', 
        read_only=True
    )

    author_id = serializers.IntegerField(
        source='author.id',
        read_only=True
    )
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'author_id',
            'content',
            'image',
            'created_at',
            'updated_at',
            'visibility'
        ]
        read_only_fields = ['id', 'created_at', 'author', 'updated_at', 'author_username', 'author_id']

    def validate_content(self, value):
        if len(value) > 280:
            raise serializers.ValidationError("Content characters cannot be greater than 280")
        return value
    
    def validate_visibility(self, value):
        VISIBILITY_CHOICES = ['public', 'private', 'followers']
        if value not in VISIBILITY_CHOICES:
            raise serializers.ValidationError("Visibility is not correct")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user
        return super().create(validated_data)
    
class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username',
        read_only=True
    )

    author_id = serializers.IntegerField(
        source='author.id',
        read_only=True
    )
    class Meta:
        model = Post
        fields = [
            'id',
            'author_username',
            'author_id',
            'content',
            'image',
            'created_at'
        ]
        read_only_fields = ['id', 'author_username', 'author_id', 'created_at']

