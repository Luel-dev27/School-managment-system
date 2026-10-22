from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name",
            "last_name",
            "teacher_id",
            "email",
            "hire_date",
            "subjects",
        ]

        read_only_fields = ["id"]
