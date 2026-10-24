from django.contrib import admin

from .models import (
    Student,
    StudentEnrollment,
    Attendance,
    StudentTransfer,
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "first_name",
        "last_name",
        "grade_level",
        "status",
        "enrollment_date",
    )

    search_fields = (
        "student_id",
        "first_name",
        "last_name",
    )

    list_filter = (
        "status",
        "grade_level",
    )


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "class_section",
        "enrollment_date",
        "status",
    )

    search_fields = (
        "student__student_id",
        "student__first_name",
        "student__last_name",
    )

    list_filter = (
        "status",
        "class_section__grade_level",
        "class_section__academic_year",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment",
        "date",
        "status",
    )

    search_fields = (
        "enrollment__student__student_id",
        "enrollment__student__first_name",
        "enrollment__student__last_name",
    )

    list_filter = (
        "status",
        "date",
    )


@admin.register(StudentTransfer)
class StudentTransferAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "transfer_date",
        "destination_school",
        "created_at",
    )

    search_fields = (
        "student__student_id",
        "student__first_name",
        "student__last_name",
        "destination_school",
    )

    list_filter = (
        "transfer_date",
    )

    readonly_fields = (
        "created_at",
    )