from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser
from projects.models import Project


class TaskCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    project = serializers.HiddenField(default=None)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'assigned_to', 'created_by', 'created_at', 'updated_at', 'updated_by']

class TasksListSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.id')
    assigned_to = serializers.ReadOnlyField(source='assigned_to.id')
    created_by = serializers.ReadOnlyField(source='created_by.id')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'assigned_to', 'created_by', 'created_at', 'updated_at', 'updated_by']
