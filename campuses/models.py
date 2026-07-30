from django.db import models


class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name


class Department(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('campus', 'name')
        

    def __str__(self):
        return f"{self.name} ({self.campus.name})"
