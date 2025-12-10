from rest_framework import permissions


class IsTenantUser(permissions.BasePermission):
    """
    Permissão para verificar se o usuário pertence ao tenant
    """
    
    def has_permission(self, request, view):
        return hasattr(request.user, 'tenant') and request.user.tenant is not None
    
    def has_object_permission(self, request, view, obj):
        # Verificar se o objeto pertence ao tenant do usuário
        if hasattr(obj, 'tenant'):
            return obj.tenant == request.user.tenant
        return False


class IsAuditorLider(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é o auditor líder da auditoria
    """
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'auditor_lider'):
            return obj.auditor_lider == request.user
        if hasattr(obj, 'auditoria'):
            return obj.auditoria.auditor_lider == request.user
        return False


class IsResponsavel(permissions.BasePermission):
    """
    Permissão para verificar se o usuário é o responsável
    """
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'responsavel'):
            return obj.responsavel == request.user
        return False


class CanEditAuditoria(permissions.BasePermission):
    """
    Permissão para editar auditoria
    Apenas auditor líder ou equipe pode editar
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'auditor_lider') and obj.auditor_lider == request.user:
            return True
        
        if hasattr(obj, 'equipe_auditores') and request.user in obj.equipe_auditores.all():
            return True
        
        return False
