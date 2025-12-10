from typing import Iterable
from rest_framework import permissions


class UserRoles:
    ADMIN = 'ADMIN'
    DIRETOR = 'DIRETOR'
    PROCESS_OWNER = 'PROCESS_OWNER'
    GESTOR = 'GESTOR'
    AUDITOR = 'AUDITOR'
    COLABORADOR = 'COLABORADOR'


def user_has_role(user, roles: Iterable[str]) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True

    perfil = getattr(user, 'perfil', None)
    if perfil and perfil in roles:
        return True

    if hasattr(user, 'groups'):
        if user.groups.filter(name__in=roles).exists():
            return True
    return False


class RolePermission(permissions.BasePermission):
    """Permission class that maps DRF actions to allowed roles."""

    def has_permission(self, request, view):
        required_roles = getattr(view, 'role_permissions', {})
        action = getattr(view, 'action', request.method.lower())
        allowed = required_roles.get(action)
        if not allowed:
            return request.user and request.user.is_authenticated
        return user_has_role(request.user, allowed)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
