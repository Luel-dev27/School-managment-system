from django.db import models

# Create your models here.
from django.db import models


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GradeLevel(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return f"Grade {self.number}"


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
