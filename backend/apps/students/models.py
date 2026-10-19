from django.db import models
from apps.academics.models import GradeLevel


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)

    grade_level = models.ForeignKey(
        GradeLevel,
        on_delete=models.PROTECT,
        related_name="students",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
