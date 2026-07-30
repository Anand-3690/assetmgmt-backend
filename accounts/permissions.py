from rest_framework.permissions import BasePermission


class IsOrgAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'org_admin'


class IsDeptAdminOrOrgAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ('org_admin', 'dept_admin')


class IsSameDepartmentObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'org_admin':
            return True
        dept = getattr(obj, 'owning_department', None) or getattr(obj.asset, 'owning_department', None)
        return dept_id_matches(dept, request.user)


def dept_id_matches(dept, user):
    return dept is not None and dept_id(dept) == user.department_id


def dept_id(dept):
    return dept.id if dept else None