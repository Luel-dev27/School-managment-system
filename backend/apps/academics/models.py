from django.db import models
from django.core.exceptions import ValidationError

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
    
    is_final_grade = models.BooleanField(default=False)

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


class Timetable(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = "monday", "Monday"
        TUESDAY = "tuesday", "Tuesday"
        WEDNESDAY = "wednesday", "Wednesday"
        THURSDAY = "thursday", "Thursday"
        FRIDAY = "friday", "Friday"

    teaching_assignment = models.ForeignKey(
        TeachingAssignment,
        on_delete=models.PROTECT,
        related_name="timetable_entries",
    )

    day_of_week = models.CharField(
        max_length=10,
        choices=DayOfWeek.choices,
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        # 1. Validate start and end time
        if self.start_time >= self.end_time:
            raise ValidationError(
                "End time must be later than start time."
            )

        # 2. Find timetable entries that overlap
        overlapping = Timetable.objects.filter(
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)

        # 3. Prevent the same class section
        # from having two lessons at the same time
        class_conflict = overlapping.filter(
            teaching_assignment__class_section=(
                self.teaching_assignment.class_section
            )
        ).exists()

        if class_conflict:
            raise ValidationError(
                "This class section already has a lesson "
                "during this time."
            )

        # 4. Prevent the same teacher
        # from teaching two classes at the same time
        teacher_conflict = overlapping.filter(
            teaching_assignment__teacher=(
                self.teaching_assignment.teacher
            )
        ).exists()

        if teacher_conflict:
            raise ValidationError(
                "This teacher already has another lesson "
                "during this time."
            )

    def __str__(self):
        return (
            f"{self.teaching_assignment} - "
            f"{self.day_of_week} "
            f"{self.start_time}-{self.end_time}"
        )