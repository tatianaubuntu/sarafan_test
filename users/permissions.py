from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """Проверяет, является ли пользователь текущим"""
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False
