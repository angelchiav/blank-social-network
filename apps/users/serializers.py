from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
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
            'bio',
            'avatar',
            'github',
            'date_joined',
            'updated_at',
            'birth_date',
            'is_active'
        ]
        read_only_fields = ['id', 'is_active', 'updated_at', 'date_joined', 'role']
        extra_kwargs = {
        'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("The username need at least 4 characters.")
        return value
    
    def validate_github(self, value):
        if not 'github.com/' in value.lower():
            raise serializers.ValidationError("The URL is not valid, NEEDS TO BE GITHUB! >:(.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("The email is already registered.")
        return value
    
    def validate_bio(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("The bio has a 300 characters limit.")
        return value
    
    def validate_role(self, value):
        ALLOWED = ['USER', 'ADMIN', 'MOD']
        if value not in ALLOWED:
            raise serializers.ValidationError("The role is not valid.")
        return value

    def validate_birth_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        if value > date.today() - timedelta(days=16*365):
            raise serializers.ValidationError("You must be at least 16 years old.")
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
            raise serializers.ValidationError("The passwords do not match.")
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

    def validate_new_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("The current password do not match.")
        return value
    
    def validate(self, data):
        pw = data.get('new_password')
        pw2 = data.get('confirm_new_password')

        if pw != pw2:
            raise serializers.ValidationError("The new passwords do not match.")
        return data
    
    def update(self, instance, validated_data):
        # Instance is the user
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
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
        email = attrs.get('email')
        password = attrs.get('password')

        # Authentication
        user = authenticate(username=email, password=password)
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