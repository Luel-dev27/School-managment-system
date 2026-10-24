from rest_framework import serializers
from .models import Student, StudentEnrollment, Attendance  


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "student_id",
            "date_of_birth",
            "enrollment_date",
            "grade_level",
            "status",
        ]
        read_only_fields = ["id", "enrollment_date", "status"]


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = [
            "id",
            "student",
            "class_section",
            "enrollment_date",
            "status",
        ]
        read_only_fields = [
            "id",
            "enrollment_date",
            "status",
        ]

    def validate(self, data):
        # --------------------------------------------------
        # 1. Existing enrollment cannot change its student.
        # --------------------------------------------------
        if self.instance and "student" in data:
            if data["student"] != self.instance.student:
                raise serializers.ValidationError(
                    {
                        "student": (
                            "The student of an existing "
                            "enrollment cannot be changed."
                        )
                    }
                )

        # --------------------------------------------------
        # 2. Historical enrollments cannot be modified.
        # --------------------------------------------------
        if self.instance and self.instance.status in [
            StudentEnrollment.Status.COMPLETED,
            StudentEnrollment.Status.TRANSFERRED,
        ]:
            protected_fields = [
                "student",
                "class_section",
            ]

            changed_fields = []

            for field in protected_fields:
                if field in data:
                    old_value = getattr(
                        self.instance,
                        field,
                    )
                    new_value = data[field]

                    if new_value != old_value:
                        changed_fields.append(field)

            if changed_fields:
                raise serializers.ValidationError(
                    {
                        "error": (
                            "Completed or transferred "
                            "enrollments cannot be modified."
                        )
                    }
                )

        # --------------------------------------------------
        # Get student and class section.
        # --------------------------------------------------
        student = data.get(
            "student",
            getattr(
                self.instance,
                "student",
                None,
            ),
        )

        class_section = data.get(
            "class_section",
            getattr(
                self.instance,
                "class_section",
                None,
            ),
        )

        # --------------------------------------------------
        # 3. Only active students can be enrolled.
        # --------------------------------------------------
        if student and student.status != Student.Status.ACTIVE:
            raise serializers.ValidationError(
                {
                    "student": (
                        "Only active students can be enrolled."
                    )
                }
            )

        # --------------------------------------------------
        # 4. Student can have only one active enrollment.
        # --------------------------------------------------
        if not self.instance and student:
            active_enrollment_exists = (
                StudentEnrollment.objects.filter(
                    student=student,
                    status=StudentEnrollment.Status.ACTIVE,
                ).exists()
            )

            if active_enrollment_exists:
                raise serializers.ValidationError(
                    {
                        "student": (
                            "This student already has an "
                            "active enrollment."
                        )
                    }
                )

        # --------------------------------------------------
        # 5. Closed academic years cannot receive
        #    new or moved enrollments.
        # --------------------------------------------------
        if class_section:
            academic_year = class_section.academic_year

            if academic_year.is_closed:
                raise serializers.ValidationError(
                    {
                        "class_section": (
                            "Students cannot be enrolled "
                            "in a closed academic year."
                        )
                    }
                )

        return data

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "enrollment",
            "date",
            "status",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        enrollment = data.get(
            "enrollment",
            getattr(self.instance, "enrollment", None),
        )

        if enrollment:
            academic_year = (
                enrollment
                .class_section
                .academic_year
            )

            if academic_year.is_closed:
                raise serializers.ValidationError(
                    {
                        "enrollment": (
                            "Attendance cannot be changed "
                            "for a closed academic year."
                        )
                    }
                )

        return data