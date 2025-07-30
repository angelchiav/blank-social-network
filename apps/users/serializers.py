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
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    