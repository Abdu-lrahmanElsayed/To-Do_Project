from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProjectCreateSerializer, ProjectSerializer
from .models import Project
from rest_framework.permissions import IsAuthenticated, IsAdminUser


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_create(request):
    serializer = ProjectCreateSerializer(data = request.data, context={'request': request})
        
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_project_list(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_project_list(request):
    projects = Project.objects.filter(owner=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_details(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if project.owner != request.user and not request.user.is_staff and not request.user.is_superuser:
        return Response({'error': 'You do not have permission to view this project'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ProjectSerializer(project, context={'request': request})
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def project_update(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    if project.owner != request.user and not request.user.is_staff and not request.user.is_superuser:
        return Response({'error': 'You do not have permission to update this project'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProjectCreateSerializer(project, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def project_delete(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    if project.owner != request.user and not request.user.is_staff and not request.user.is_superuser:
        return Response({'error': 'You do not have permission to delete this project'}, status=status.HTTP_403_FORBIDDEN)

    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)