from rest_framework import serializers
from .models import Project


class ProjectCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'expected_completion_date', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    #owner = serializers.StringRelatedField()
    owner = serializers.ReadOnlyField(source='owner.id')
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'expected_completion_date', 'updated_at']