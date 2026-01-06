from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project
from accounts.models import CustomUser
from .models import Task
from .serializers import TasksListSerializer, TaskCreateSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    assigned_to = get_object_or_404(CustomUser, id=request.data.get('assigned_to'))
    serializer = TaskCreateSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save(project=project, assigned_to=assigned_to)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    if request.user != project.owner:
        tasks = tasks.filter(assigned_to=request.user)

    serializer = TasksListSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_details(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)

    if request.user != project.owner and request.user != task.assigned_to:
        return Response({'detail': 'Not authorized to view this task.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = TasksListSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def task_update(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)

    if request.user != project.owner and request.user != task.assigned_to:
        return Response({'detail': 'Not authorized to update this task.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = TaskCreateSerializer(task, data=request.data, partial=True, context={'request': request})

    if serializer.is_valid():
        serializer.save(updated_by=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def task_delete(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)

    if request.user != project.owner:
        return Response({'detail': 'Not authorized to delete this task.'}, status=status.HTTP_403_FORBIDDEN)

    task.delete()
    return Response({'detail': 'Task deleted successfully.'}, status=status.HTTP_200_OK)