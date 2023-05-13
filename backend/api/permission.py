from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
