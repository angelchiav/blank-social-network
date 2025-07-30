from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MOD', 'Moderator'),
        ('USER', 'User')
    ]
    bio = models.TextField(
        'Bio',
        blank=True,
        null=True,
        help_text='Optional'
    )

    avatar = models.ImageField(
        'Profile Picture',
        upload_to='profile_pics/',
        null=True,
        blank=True,
        help_text='Optional'
    )

    role = models.CharField(
        max_length=40,
        choices=ROLE_CHOICES,
        default='USER'
    )

    date_joined = models.DateTimeField(
        'Date Joined',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Updated At',
        auto_now=True
    )

    github = models.URLField(
        'GitHub',
        blank=True,
        null=True,
        help_text='Optional'
    )

    birth_date = models.DateTimeField(
        'Birth Date',
        blank=True,
        null=True,
        help_text='Optional'
    )

    is_active = models.BooleanField(
        'Is Active',
        default=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"