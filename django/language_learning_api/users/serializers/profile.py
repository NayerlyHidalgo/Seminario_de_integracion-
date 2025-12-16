# users/serializers/profile.py
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'streak_count', 'total_study_time', 'created_at', 'updated_at')
    
    def update(self, instance, validated_data):
        # Update user fields if provided
        user_data = self.initial_data.get('user_data', {})
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        
        return super().update(instance, validated_data)