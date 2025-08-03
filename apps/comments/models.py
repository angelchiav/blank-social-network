from django.db import models
from django.conf import settings
from apps.posts.models import Post
from django.core.exceptions import ValidationError

class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField(
        max_length=280
    )

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['parent'])
        ]

    def clean(self):
        if self.post.visibility == 'private' and self.post.author != self.author:
            if not self.post.author.followers.filter(from_user=self.author).exists():
                raise ValidationError(
                    "Cannot comment in private posts."
                )
        
        if self.parent:
            depth = 0
            current = self.parent
            while current.parent and depth < 3:
                current = current.parent
                depth += 1
            if depth >= 3:
                raise ValidationError(
                    "Maximum nesting depth reached."
                )

    @property
    def is_reply(self):
        return self.parent is not None
    
    @property
    def get_thread_depth(self):
        depth = 0
        current = self.parent
        while current:
            depth += 1
            current = current.parent
        return depth
    
    @property
    def get_description(self):
        if self.is_reply:
            return f"Reply by {self.author.username} to {self.parent.author.username}"
        return f"Comment by {self.author.username} on post {self.post.id}"

    def __str__(self):
        return f"Comment by {self.author.username}"