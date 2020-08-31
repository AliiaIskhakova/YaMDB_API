"""

Remark for reviewer:
rewrite custom permission.

"""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from auth_user.models import Role


class IsAuthenticatedOrAdminOrModeratorOrAuthor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.role == Role.ADMIN or
            request.user.role == Role.MODERATOR or
            obj.author == request.user)
