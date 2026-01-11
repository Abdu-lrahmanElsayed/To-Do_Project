from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the owner of the object or an admin
        return obj.owner == request.user or request.user.is_staff or request.user.is_superuser