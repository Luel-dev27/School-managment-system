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
        fields = [
            "id",
            "number",
            "is_final_grade",
        ]
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
            "is_closed",
        ]
        read_only_fields = [
            "id",
            "is_current",
            "is_closed",
       ]

    def validate(self, data):
        start_date = data.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )

        end_date = data.get(
            "end_date",
            getattr(self.instance, "end_date", None),
        )

        is_current = data.get(
            "is_current",
            getattr(self.instance, "is_current", False),
        )

        is_closed = data.get(
            "is_closed",
            getattr(self.instance, "is_closed", False),
        )

        # End date must be later than start date.
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError({
                "end_date": (
                    "End date must be later than start date."
                )
            })

        # A closed academic year cannot also be current.
        if is_current and is_closed:
            raise serializers.ValidationError({
                "is_closed": (
                    "A closed academic year cannot be current."
                )
            })

        # Only one academic year can be current.
        if is_current:
            current_years = AcademicYear.objects.filter(
                is_current=True
            )

            if self.instance:
                current_years = current_years.exclude(
                    pk=self.instance.pk
                )

            if current_years.exists():
                raise serializers.ValidationError({
                    "is_current": (
                        "Only one academic year can be current."
                    )
                })

        return data

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

    def validate(self, data):
        academic_year = data.get(
            "academic_year",
            getattr(self.instance, "academic_year", None),
        )

        if academic_year and academic_year.is_closed:
            raise serializers.ValidationError(
                {
                    "academic_year": (
                        "Class sections cannot be created "
                        "or changed in a closed academic year."
                    )
                }
            )

        return data
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

    def validate(self, data):
        class_section = data.get(
            "class_section",
            getattr(self.instance, "class_section", None),
        )

        if class_section:
            academic_year = class_section.academic_year

            if academic_year.is_closed:
                raise serializers.ValidationError(
                    {
                        "class_section": (
                            "Teaching assignments cannot be "
                            "created or changed in a closed "
                            "academic year."
                        )
                    }
                )

        return data


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

    def validate(self, data):
        enrollment = data.get(
            "enrollment",
            getattr(self.instance, "enrollment", None),
        )

        subject = data.get(
            "subject",
            getattr(self.instance, "subject", None),
        )

        # Do not allow results to be created or updated
        # for a closed academic year.
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
                            "Results cannot be changed "
                            "for a closed academic year."
                        )
                    }
                )

        # The subject must be assigned to the
        # student's class section.
        if enrollment and subject:
            subject_is_assigned = (
                TeachingAssignment.objects.filter(
                    class_section=enrollment.class_section,
                    subject=subject,
                ).exists()
            )

            if not subject_is_assigned:
                raise serializers.ValidationError(
                    {
                        "subject": (
                            "This subject is not assigned "
                            "to the student's class section."
                        )
                    }
                )

        return data


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