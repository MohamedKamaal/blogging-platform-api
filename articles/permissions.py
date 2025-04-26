from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission that:
    - Allows read-only access to all users (GET, HEAD, OPTIONS)
    - Grants write access only to the author of the object (POST, PUT, PATCH, DELETE)
    - Requires authentication for write operations
    """

    def has_permission(self, request, view):
        """
        Global permission check for list/create actions.
        - Safe methods allowed to all
        - Write methods require authentication
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-specific permission check.
        - Safe methods allowed to all
        - Write methods require user to be the author
        """
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Explicitly check for is_authenticated for security
        if not request.user or not request.user.is_authenticated:
            return False
            
        return obj.author == request.user