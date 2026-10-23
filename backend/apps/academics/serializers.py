from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import (AcademicYear, 
                     GradeLevel, 
                     Subject, 
                     ClassSection, 
                     TeachingAssignment, 
                     Result,
                     Timetable,
                        )


class GradeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevel
        fields = ["id", "number"]
        read_only_fields = ["id"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name", "code"]
        read_only_fields = ["id"]


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "is_current",
        ]
        read_only_fields = ["id"]

class ClassSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSection
        fields = [
            "id",
            "grade_level",
            "academic_year",
            "name",
        ]
        read_only_fields = ["id"]


class TeachingAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingAssignment
        fields = [
            "id",
            "teacher",
            "subject",
            "class_section",
        ]
        read_only_fields = ["id"]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            "id",
            "enrollment",
            "subject",
            "term",
            "score",
        ]
        read_only_fields = ["id"]

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Score must be between 0 and 100."
            )

        return value


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = [
            "id",
            "teaching_assignment",
            "day_of_week",
            "start_time",
            "end_time",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        timetable = Timetable(
            teaching_assignment=data.get(
                "teaching_assignment",
                getattr(
                    self.instance,
                    "teaching_assignment",
                    None,
                ),
            ),
            day_of_week=data.get(
                "day_of_week",
                getattr(
                    self.instance,
                    "day_of_week",
                    None,
                ),
            ),
            start_time=data.get(
                "start_time",
                getattr(
                    self.instance,
                    "start_time",
                    None,
                ),
            ),
            end_time=data.get(
                "end_time",
                getattr(
                    self.instance,
                    "end_time",
                    None,
                ),
            ),
        )

        # Important for PATCH/PUT:
        # exclude the current timetable from conflict checking.
        if self.instance:
            timetable.pk = self.instance.pk

        try:
            timetable.clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                error.messages
            )

        return data