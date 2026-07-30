from django.db import models


class DepartmentScopedQuerySet(models.QuerySet):
    def for_user(self, user):
        if user.role == 'org_admin':
            return self
        return self.filter(owning_department=user.department)


# assets/querysets.py
# assets/querysets.py
class DepartmentScopedViewSetMixin:
    def get_queryset(self):
        return self.queryset.for_user(self.request.user)