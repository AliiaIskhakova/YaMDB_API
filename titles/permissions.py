from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_staff or request.user.is_superuser)
