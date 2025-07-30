from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MOD', 'Moderator'),
        ('USER', 'User')
    ]

    role = models.CharField(
        max_length=40,
        choices=ROLE_CHOICES,
        default='USER'
    )
    
    avatar = models.ImageField(
        'Profile Picture',
        upload_to='profile_pics/',
        null=True,
        blank=True,
        help_text='Optional'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )

    bio = models.TextField(
        'Bio',
        blank=True,
        null=True,
        help_text='Optional'
    )

    github = models.URLField(
        'GitHub',
        blank=True,
        null=True,
        help_text='Optional'
    )

    birth_date = models.DateField(
        'Birth Date',
        blank=True,
        null=True,
        help_text='Optional'
    )

    updated_at = models.DateTimeField(
        'Updated At',
        auto_now=True
    )

class Relationship(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='From user',
        related_name='following'
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='To user',
        related_name='followers'
    )
    
    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True
    )
    class Meta:
        unique_together = (('from_user', 'to_user'),)
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    token = models.CharField(
        'Verification Token',
        max_length=64,
        unique=True,
        help_text='Unique token for email verification'
    )
    
    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True
    )

    used = models.BooleanField(
        'The token is used',
        default=False
    )
