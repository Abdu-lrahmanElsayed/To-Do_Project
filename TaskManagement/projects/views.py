from .serializers import ProjectCreateSerializer, ProjectSerializer
from .models import Project
from rest_framework import viewsets
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(owner=user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)