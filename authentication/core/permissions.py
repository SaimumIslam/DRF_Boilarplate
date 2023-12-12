from rest_framework import permissions

from ..utils.role import ADMIN_ROLES, EMPLOYEE_ROLES
from ..services.permission import PermissionService


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "SA"


class IsInstituteAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "IA"


class IsBranchAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "BA"


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "TC"


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "SF"


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "AG"


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ST"


class IsAdmins(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ADMIN_ROLES


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in EMPLOYEE_ROLES


class IsAdminsOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ADMIN_ROLES


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in EMPLOYEE_ROLES


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, instance):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return instance.created_by == request.user


class HasApiPermissions(permissions.BasePermission):
    permission_service = PermissionService()

    code_name_map = {
        'GET': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
        'DELETE': 'delete',
    }

    def _get_permission_codename(self, method, model_cls):
        if method not in self.code_name_map.keys():
            return ""

        # app_label = model_cls._meta.app_label
        model_name = model_cls._meta.model_name
        code_name = f"{self.code_name_map[method]}_{model_name}"

        return code_name

    def _queryset(self, view):
        if hasattr(view, 'get_queryset'):
            return view.get_queryset()
        return view.queryset

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if getattr(view, '_ignore_model_permissions', False):
            return True

        queryset = self._queryset(view)
        codename = self._get_permission_codename(request.method, queryset.model)

        has_permission = self.permission_service.has_all_including_group_permissions_by_user__codename(request.user, codename)

        return has_permission
