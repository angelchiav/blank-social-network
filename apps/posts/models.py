from django.db import models
from django.conf import settings

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('followers', 'Followers'),
        ('private', 'Private')
    ]
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    
    content = models.TextField(
        max_length=280
    )

    image = models.ImageField(
        upload_to='posts/images',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='private'
    )
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post {self.id} by {self.author.username}'
    
class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ['user', 'post'] # One user can like a post just once
    