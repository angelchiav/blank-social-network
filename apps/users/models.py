from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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
        
    def clean(self):
        if self.avatar and self.avatar.size > 2 * 1024 * 1024:
            raise ValidationError(
                "Avatar too large."
            )
        
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_short_name(self):
        return f"{self.first_name}"

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

    created_at = models.DateTimeField(
        'Created At',
        auto_now_add=True
    )
    
    @property
    def age(self):
        from datetime import date
        if not self.birth_date:
            return None
        return (date.today() - self.birth_date).days // 365

    def clean(self):
        if self.birth_date and self.age < 16:
            raise ValidationError(
                "User must be at least 16 years old."
            )
    
    def __str__(self):
        return f"{self.user.username.capitalize()}'s Profile"
        
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

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError(
                "User cannot follow themselves."
            )

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}."
        
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

    def __str__(self):
        return f"Token for {self.user.email} (used: {self.used})"