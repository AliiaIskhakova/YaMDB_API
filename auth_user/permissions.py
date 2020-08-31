from rest_framework.permissions import BasePermission

from .models import Role


class IsOwnerProfileOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(
                request.user.is_staff or request.user.role == Role.ADMIN)
