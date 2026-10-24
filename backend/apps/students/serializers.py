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
        read_only_fields = ["id", "enrollment_date", "status"]


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