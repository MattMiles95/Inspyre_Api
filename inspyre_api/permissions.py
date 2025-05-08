from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission class that allows object modification only if the
    requesting user is the owner.

    - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for any user.
    - Modification methods (POST, PUT, PATCH, DELETE) are restricted to the
    owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the request has permission to modify the object.

        Returns True for safe methods. For modification methods, checks if the
        requesting user is the owner of the object.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
