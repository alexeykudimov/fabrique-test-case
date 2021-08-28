from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    # Права суперпользователя
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
