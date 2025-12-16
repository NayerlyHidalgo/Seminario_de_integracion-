# languages/serializers/language.py
from rest_framework import serializers
from languages.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    difficulty_text = serializers.CharField(read_only=True)
    
    class Meta:
        model = Language
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_code(self, value):
        """Ensure language code is lowercase"""
        return value.lower()

    def validate_difficulty_level(self, value):
        """Ensure difficulty level is between 1 and 5"""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Difficulty level must be between 1 and 5")
        return value