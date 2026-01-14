from rest_framework import permissions
from projects.models import Project


class IsAssigned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user
 
class IsProjectOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # Require authentication for any project-level action
        if not user or not user.is_authenticated:
            return False
        # Allow staff and superusers for all actions
        if user.is_staff or user.is_superuser:
            return True
        # For non-object actions (list, create) enforce project ownership
        if view.action in ('list', 'create'):
            project_pk = view.kwargs.get('project_pk') or request.data.get('project') or request.query_params.get('project')
            if not project_pk:
                return False
            try:
                project = Project.objects.get(pk=project_pk)
            except Project.DoesNotExist:
                return False
            return project.owner == user
        # For other actions (detail actions) defer to object-level checks
        return True

    def has_object_permission(self, request, view, obj):
        return obj.project.owner == request.user or request.user.is_staff or request.user.is_superuser
    