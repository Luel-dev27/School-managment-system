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
        read_only_fields = ["id", "enrollment_date", "grade_level", "status"]


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
        # 1. Once an enrollment is created, its student
        #    cannot be changed.
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
        # 2. Once an enrollment is created, its class
        #    section cannot be changed directly.
        #
        #    Student movement must use the dedicated
        #    lifecycle workflows:
        #    promote, repeat, transfer, or graduate.
        # --------------------------------------------------
        if self.instance and "class_section" in data:
            if data["class_section"] != self.instance.class_section:
                raise serializers.ValidationError(
                    {
                        "class_section": (
                            "The class section of an existing "
                            "enrollment cannot be changed. "
                            "Use the student lifecycle "
                            "workflow instead."
                        )
                    }
                )

        # --------------------------------------------------
        # Get the student and class section.
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
        # 4. A student can have only one active enrollment.
        #    This validation gives a clean API error.
        #    The database constraint remains the final
        #    safety layer.
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
        # 5. New enrollments cannot be created inside
        #    a closed academic year.
        # --------------------------------------------------
        if not self.instance and class_section:
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
        # --------------------------------------------------
        # 1. Once attendance is created, its enrollment
        #    cannot be changed.
        #
        #    An attendance record belongs permanently to
        #    the student's original enrollment.
        # --------------------------------------------------
        if self.instance and "enrollment" in data:
            if data["enrollment"] != self.instance.enrollment:
                raise serializers.ValidationError(
                    {
                        "enrollment": (
                            "The enrollment of an existing "
                            "attendance record cannot be changed."
                        )
                    }
                )

        # --------------------------------------------------
        # Get enrollment.
        # For PATCH, enrollment may not be included,
        # so use the existing enrollment.
        # --------------------------------------------------
        enrollment = data.get(
            "enrollment",
            getattr(
                self.instance,
                "enrollment",
                None,
            ),
        )

        # --------------------------------------------------
        # Get attendance date.
        # For PATCH, date may not be included,
        # so use the existing date.
        # --------------------------------------------------
        attendance_date = data.get(
            "date",
            getattr(
                self.instance,
                "date",
                None,
            ),
        )

        if enrollment:
            academic_year = (
                enrollment
                .class_section
                .academic_year
            )

            # --------------------------------------------------
            # 2. Attendance cannot be created or changed
            #    for a closed academic year.
            # --------------------------------------------------
            if academic_year.is_closed:
                raise serializers.ValidationError(
                    {
                        "enrollment": (
                            "Attendance cannot be changed "
                            "for a closed academic year."
                        )
                    }
                )

            # --------------------------------------------------
            # 3. Attendance date must belong to the
            #    enrollment's academic year.
            # --------------------------------------------------
            if attendance_date:
                if not (
                    academic_year.start_date
                    <= attendance_date
                    <= academic_year.end_date
                ):
                    raise serializers.ValidationError(
                        {
                            "date": (
                                "Attendance date must be "
                                "within the enrollment's "
                                "academic year."
                            )
                        }
                    )

        return data