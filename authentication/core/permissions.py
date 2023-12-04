from rest_framework import permissions
from authentication.utils.role import ADMIN_ROLES, EMPLOYEE_ROLES


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
