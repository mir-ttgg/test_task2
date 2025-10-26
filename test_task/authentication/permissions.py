from rest_framework import permissions

from .models import Permission, UserRole


class HasResourcePermission(permissions.BasePermission):
    """
    Кастомное разрешение для проверки доступа к ресурсам
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not request.user.is_active:
            return False
        resource_name = getattr(view, 'resource_name', None)
        action_name = getattr(view, 'action_name', None)

        if not resource_name or not action_name:
            return True

        return self._check_user_permission(request.user,
                                           resource_name, action_name)

    def _check_user_permission(self, user, resource_name, action_name):
        """Проверяет, есть ли у пользователя разрешение"""
        try:

            user_roles = UserRole.objects.filter(
                user=user).values_list('role', flat=True)
            permission_exists = Permission.objects.filter(
                role__in=user_roles,
                resource__name=resource_name,
                action__name=action_name
            ).exists()

            return permission_exists

        except Exception:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение только для владельца объекта или только для чтения
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение только для администраторов или только для чтения
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
