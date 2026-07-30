from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('org_admin', 'Org Admin'),
        ('dept_admin', 'Department Admin'),
        ('dept_member', 'Department Member'),
    ]
    department = models.ForeignKey(
        'campuses.Department', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='users',
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='dept_member')

    def __str__(self):
        return self.username