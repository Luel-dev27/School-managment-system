from django.db import models

# Create your models here.

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

class ClassSection(models.Model):
    grade_level = models.ForeignKey(
        GradeLevel,
        on_delete=models.PROTECT,
        related_name="sections",
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="class_sections",
    )

    name = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["grade_level", "academic_year", "name"],
                name="unique_section_per_grade_year",
            )
        ]
        ordering = ["grade_level__number", "name"]

    def __str__(self):
        return (
            f"Grade {self.grade_level.number}{self.name} "
            f"({self.academic_year.name})"
        )

class TeachingAssignment(models.Model):
    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    class_section = models.ForeignKey(
        ClassSection,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "subject", "class_section"],
                name="unique_teacher_subject_section",
            )
        ]

    def __str__(self):
        return (
            f"{self.teacher} - {self.subject} - "
            f"{self.class_section}"
        )


class Result(models.Model):
    class Term(models.TextChoices):
        TERM_1 = "term_1", "Term 1"
        TERM_2 = "term_2", "Term 2"

    enrollment = models.ForeignKey(
        "students.StudentEnrollment",
        on_delete=models.PROTECT,
        related_name="results",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="results",
    )

    term = models.CharField(
        max_length=10,
        choices=Term.choices,
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "subject", "term"],
                name="unique_student_subject_term_result",
            )
        ]

    def __str__(self):
        return (
            f"{self.enrollment.student} - "
            f"{self.subject} - "
            f"{self.term}: {self.score}"
        )