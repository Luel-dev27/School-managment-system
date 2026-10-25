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
        # Current and closed academic years have
        # protected historical/lifecycle metadata.
        if self.instance and (
            self.instance.is_current
            or self.instance.is_closed
        ):
            protected_fields = [
                "name",
                "start_date",
                "end_date",
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
                if self.instance.is_closed:
                    message = (
                        "A closed academic year cannot "
                        "be modified."
                    )
                else:
                    message = (
                        "The current academic year cannot "
                        "be modified."
                    )

                raise serializers.ValidationError(
                    {
                        "error": message
                    }
                )

        start_date = data.get(
            "start_date",
            getattr(
                self.instance,
                "start_date",
                None,
            ),
        )

        end_date = data.get(
            "end_date",
            getattr(
                self.instance,
                "end_date",
                None,
            ),
        )

        is_current = data.get(
            "is_current",
            getattr(
                self.instance,
                "is_current",
                False,
            ),
        )

        is_closed = data.get(
            "is_closed",
            getattr(
                self.instance,
                "is_closed",
                False,
            ),
        )

        # End date must be later than start date.
        if (
            start_date
            and end_date
            and start_date >= end_date
        ):
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "End date must be later than "
                        "start date."
                    )
                }
            )

        # A closed academic year cannot also be current.
        if is_current and is_closed:
            raise serializers.ValidationError(
                {
                    "is_closed": (
                        "A closed academic year cannot "
                        "be current."
                    )
                }
            )

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
                raise serializers.ValidationError(
                    {
                        "is_current": (
                            "Only one academic year can "
                            "be current."
                        )
                    }
                )

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
        # -----------------------------------------------
        # Protect the identity of an existing section.
        # -----------------------------------------------
        if self.instance:
            if "grade_level" in data:
                if (
                    data["grade_level"]
                    != self.instance.grade_level
                ):
                    raise serializers.ValidationError(
                        {
                            "grade_level": (
                                "The grade level of an existing "
                                "class section cannot be changed."
                            )
                        }
                    )

            if "academic_year" in data:
                if (
                    data["academic_year"]
                    != self.instance.academic_year
                ):
                    raise serializers.ValidationError(
                        {
                            "academic_year": (
                                "The academic year of an existing "
                                "class section cannot be changed."
                            )
                        }
                    )

        # -----------------------------------------------
        # Protect closed academic years.
        # -----------------------------------------------
        academic_year = data.get(
            "academic_year",
            getattr(
                self.instance,
                "academic_year",
                None,
            ),
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
        # -----------------------------------------------
        # Protect the identity of an existing assignment.
        # -----------------------------------------------
        if self.instance:
            if "teacher" in data:
                if data["teacher"] != self.instance.teacher:
                    raise serializers.ValidationError(
                        {
                            "teacher": (
                                "The teacher of an existing "
                                "teaching assignment cannot "
                                "be changed."
                            )
                        }
                    )

            if "subject" in data:
                if data["subject"] != self.instance.subject:
                    raise serializers.ValidationError(
                        {
                            "subject": (
                                "The subject of an existing "
                                "teaching assignment cannot "
                                "be changed."
                            )
                        }
                    )

            if "class_section" in data:
                if (
                    data["class_section"]
                    != self.instance.class_section
                ):
                    raise serializers.ValidationError(
                        {
                            "class_section": (
                                "The class section of an existing "
                                "teaching assignment cannot "
                                "be changed."
                            )
                        }
                    )

        # -----------------------------------------------
        # Protect closed academic years.
        # -----------------------------------------------
        class_section = data.get(
            "class_section",
            getattr(
                self.instance,
                "class_section",
                None,
            ),
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
        # Score must always be between 0 and 100.
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Score must be between 0 and 100."
            )

        return value

    def validate(self, data):
        # --------------------------------------------------
        # 1. Existing result enrollment cannot be changed.
        # --------------------------------------------------
        if self.instance and "enrollment" in data:
            if data["enrollment"] != self.instance.enrollment:
                raise serializers.ValidationError(
                    {
                        "enrollment": (
                            "The enrollment of an existing "
                            "result cannot be changed."
                        )
                    }
                )

        # --------------------------------------------------
        # 2. Existing result subject cannot be changed.
        # --------------------------------------------------
        if self.instance and "subject" in data:
            if data["subject"] != self.instance.subject:
                raise serializers.ValidationError(
                    {
                        "subject": (
                            "The subject of an existing "
                            "result cannot be changed."
                        )
                    }
                )

        # --------------------------------------------------
        # 3. Existing result term cannot be changed.
        # --------------------------------------------------
        if self.instance and "term" in data:
            if data["term"] != self.instance.term:
                raise serializers.ValidationError(
                    {
                        "term": (
                            "The term of an existing "
                            "result cannot be changed."
                        )
                    }
                )

        # --------------------------------------------------
        # Get enrollment and subject.
        #
        # During PATCH they may not be included, so use
        # the values from the existing result.
        # --------------------------------------------------
        enrollment = data.get(
            "enrollment",
            getattr(
                self.instance,
                "enrollment",
                None,
            ),
        )

        subject = data.get(
            "subject",
            getattr(
                self.instance,
                "subject",
                None,
            ),
        )

        # --------------------------------------------------
        # 4. Results cannot be created or updated
        #    in a closed academic year.
        # --------------------------------------------------
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

        # --------------------------------------------------
        # 5. The subject must actually be assigned to
        #    the student's class section.
        # --------------------------------------------------
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
        # --------------------------------------------------
        # 1. An existing timetable entry cannot be moved
        #    to another teaching assignment.
        # --------------------------------------------------
        if self.instance and "teaching_assignment" in data:
            if (
                data["teaching_assignment"]
                != self.instance.teaching_assignment
            ):
                raise serializers.ValidationError(
                    {
                        "teaching_assignment": (
                            "The teaching assignment of an "
                            "existing timetable entry cannot "
                            "be changed."
                        )
                    }
                )

        # --------------------------------------------------
        # Get teaching assignment.
        # For PATCH, use the existing value when it is
        # not included in the request.
        # --------------------------------------------------
        teaching_assignment = data.get(
            "teaching_assignment",
            getattr(
                self.instance,
                "teaching_assignment",
                None,
            ),
        )

        # --------------------------------------------------
        # 2. Protect closed academic years.
        # --------------------------------------------------
        if teaching_assignment:
            academic_year = (
                teaching_assignment
                .class_section
                .academic_year
            )

            if academic_year.is_closed:
                raise serializers.ValidationError(
                    {
                        "teaching_assignment": (
                            "Timetable entries cannot be "
                            "created or changed in a closed "
                            "academic year."
                        )
                    }
                )

        # --------------------------------------------------
        # Build a temporary timetable object so the model's
        # clean() method can check:
        #
        # - start time < end time
        # - class-section conflicts
        # - teacher conflicts
        # --------------------------------------------------
        timetable = Timetable(
            teaching_assignment=teaching_assignment,
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

        # --------------------------------------------------
        # 3. When updating an existing timetable entry,
        #    exclude that same entry from conflict checking.
        # --------------------------------------------------
        if self.instance:
            timetable.pk = self.instance.pk

        try:
            timetable.clean()

        except DjangoValidationError as error:
            raise serializers.ValidationError(
                error.messages
            )

        return data