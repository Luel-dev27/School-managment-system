from django.db import models
from apps.academics.models import Subject


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    hire_date = models.DateField()

    subjects = models.ManyToManyField(
        Subject,
        related_name="teachers",
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
