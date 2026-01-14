from rest_framework import viewsets
from .serializers import TasksListSerializer, TaskCreateSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProjectOwnerOrAdmin, IsAssigned
from .models import Task
from django.shortcuts import get_object_or_404
from projects.models import Project


class TaskViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsAssigned | IsProjectOwnerOrAdmin]
        elif self.action in ['destroy', 'list', 'create']:
            self.permission_classes = [IsAuthenticated, IsProjectOwnerOrAdmin]
        return super().get_permissions()

    def get_queryset(self):
        """
        Return tasks visible to the requesting user, optionally filtered by
        a project id provided either as a URL kwarg `project_pk` (from
        nested routes) or a query parameter `?project=<id>`.
        """
        project_pk = self.kwargs.get('project_pk') or self.request.query_params.get('project')
        if project_pk:
            return Task.objects.filter(project__id=project_pk)
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(project__owner=user) | Task.objects.filter(assigned_to=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateSerializer
        return TasksListSerializer

    def perform_create(self, serializer):
        # Prefer project from nested URL (project_pk) or fall back to request data
        project_pk = self.kwargs.get('project_pk') or self.request.data.get('project')
        if project_pk:
            project = get_object_or_404(Project, pk=project_pk)
            serializer.save(project=project)
        else:
            # If no project specified, let serializer attempt to save (may raise IntegrityError)
            serializer.save()