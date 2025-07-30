from rest_framework import serializers
from .models import User

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

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The passwords do not match")
        return data
    
    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("The username need at least 4 characters")
        return value
    
    def validate_github(self, value):
        if not 'github.com/' in value.lower():
            raise serializers.ValidationError("The URL is not valid, NEEDS TO BE GITHUB! >:(")
        return value
    
    def validate_email(self, value):
        if not '@' and '.' and not value.isdigit():
            raise serializers.ValidationError("The email is not valid")
        return value
    
    def validate_bio(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("The bio has a 300 characters limit")
        return value
    
    def validate_role(self, value):
        ALLOWED = ['USER', 'ADMIN', 'MOD']
        if value not in ALLOWED:
            raise serializers.ValidationError("The role is not valid")
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
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user