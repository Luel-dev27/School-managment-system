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
        read_only_fields = ["id", "enrollment_date"]


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