# catalog/serializers/language.py
from rest_framework import serializers
from catalog.models import Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'slug', 'code', 'flag_icon', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    def create(self, validated_data):
        return Language.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance