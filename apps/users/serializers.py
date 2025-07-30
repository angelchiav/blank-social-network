from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile, Relationship, EmailVerificationToken
from datetime import date, timedelta
from django.contrib.auth import authenticate, get_user_model

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        max_length=40,
        write_only=True,
        style={'input_type': 'password'}
        )
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
            'role',
            'date_joined',
            'is_active',
            'avatar'
        ]
        read_only_fields = ['id', 'is_active', 'updated_at', 'role']
        extra_kwargs = {
        'password': {'write_only': True, 'style': {'input_type': 'password'}},
        'avatar': {'required': False}
        }

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value
    
    def validate_role(self, value):
        ALLOWED = ['USER', 'ADMIN', 'MOD']
        if value not in ALLOWED:
            raise serializers.ValidationError("Role is not valid.")
        return value

    def validate_password(self, value):
        import re
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PublicUserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    class Meta:    
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'date_joined',
            'post_count',
            'follower_count',
            'following_count'
        ]
        read_only_fields = ['id', 'date_joined', 'post_count', 'follower_count', 'following_count']

    def get_post_count(self, obj):
        return obj.posts.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()
    
class UserListSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'post_count'
        ]
        read_only_fields = ['id', 'post_count']
    
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )

    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )

    confirm_new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password does not match.")
        return value
    
    def validate_new_password(self, value):
        import re
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, data):
        pw = data.get('new_password')
        pw2 = data.get('confirm_new_password')

        if pw != pw2:
            raise serializers.ValidationError("New passwords do not match.")
        return data
    
    def update(self, instance, validated_data):
        # Instance is the user
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        write_only=True
    )

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )

    access = serializers.CharField(
        read_only=True
    )

    refresh = serializers.CharField(
        read_only=True
    )

    user = PublicUserSerializer(
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Authentication
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.", code='authorization')
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.", code='authorization')
        
        # Generating Tokens
        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        # Serializing public data of user
        attrs['user'] = PublicUserSerializer(user, context=self.context).data

        return attrs
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Profile
        fields = [
            'bio',
            'github',
            'birth_date',
            'updated_at',
        ]
        read_only_fields = ['updated_at']
        extra_kwargs = {
            'bio': {'required': False},
            'github': {'required': False},
            'birth_date': {'required': False},
        }

    def validate_bio(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("Bio cannot exceed 300 characters.")
        return value
    
    def validate_github(self, value):
        if 'github.com' not in value:
            raise serializers.ValidationError("GitHub URL must be valid.")
        return value

    def validate_birth_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        if value > date.today() - timedelta(days=16*365):
            raise serializers.ValidationError("User must be at least 16 years old.")
        return value

class FollowerSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    class Meta:
        model = Relationship
        fields = [
            'id',
            'created_at',
            'follower'
        ]
        read_only_fields = fields

    def get_follower(self, obj):
        return {
            'id': obj.from_user.id,
            'username': obj.from_user.username,
            'avatar': obj.from_user.avatar if obj.from_user.avatar else None
        }

class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    class Meta:
        model = Relationship
        fields = [
            'id',
            'created_at',
            'following'
        ]
        read_only_fields = fields
    
    def get_following(self, obj):
        return {
            'id': obj.to_user.id,
            'username': obj.to_user.username,
            'avatar': obj.to_user.avatar if obj.to_user.avatar else None
        }
    
class EmailVerificationTokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            ev = EmailVerificationToken.objects.get(token=value, used=False)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired verification token.")
        return ev
    
    def save(self, *args, **kwargs):
        ev = self.validated_data['token']
        user = ev.user
        user.email_verified = True
        user.is_active = True
        user.save(update_fields=['email_verified', 'is_active'])
        ev.used = True
        ev.save(update_fields=['used'])
        return user