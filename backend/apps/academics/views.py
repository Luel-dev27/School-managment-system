from django.shortcuts import render

# Create your views here.
from django.db import transaction
from apps.students.models import Student, StudentEnrollment
from rest_framework.decorators import api_view, permission_classes
from apps.accounts.permissions import CanAccessResults, CanAccessAcademics, CanAccessStudents
from rest_framework.response import Response
from rest_framework import status

from .models import (AcademicYear,
        GradeLevel, 
        Subject, 
        ClassSection, 
        TeachingAssignment, 
        Result,
        Timetable)

from .serializers import (
    AcademicYearSerializer,
    GradeLevelSerializer,
    SubjectSerializer,
    ClassSectionSerializer,
    TeachingAssignmentSerializer,
    ResultSerializer,
    TimetableSerializer,
)


# -------------------------
# Grade Levels API
# -------------------------

@api_view(["GET", "POST"])
@permission_classes([CanAccessAcademics])
def grade_list(request):
    if request.method == "GET":
        grades = GradeLevel.objects.all().order_by("number")
        serializer = GradeLevelSerializer(grades, many=True)
        return Response(serializer.data)

    serializer = GradeLevelSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessAcademics])
def grade_detail(request, grade_id):
    try:
        grade = GradeLevel.objects.get(id=grade_id)
    except GradeLevel.DoesNotExist:
        return Response(
            {"error": "Grade level not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = GradeLevelSerializer(grade)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = GradeLevelSerializer(
            grade,
            data=request.data,
        )

    elif request.method == "PATCH":
        serializer = GradeLevelSerializer(
            grade,
            data=request.data,
            partial=True,
        )

    if request.method in ["PUT", "PATCH"]:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "DELETE":
        try:
            grade.delete()
        except Exception:
            return Response(
                {
                    "error": (
                        "This grade level cannot be deleted "
                        "because other records may depend on it."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------
# Subjects API
# -------------------------

@api_view(["GET", "POST"])
@permission_classes([CanAccessAcademics])
def subject_list(request):
    if request.method == "GET":
        subjects = Subject.objects.all().order_by("name")
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    serializer = SubjectSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessAcademics])
def subject_detail(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return Response(
            {"error": "Subject not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = SubjectSerializer(
            subject,
            data=request.data,
        )

    elif request.method == "PATCH":
        serializer = SubjectSerializer(
            subject,
            data=request.data,
            partial=True,
        )

    if request.method in ["PUT", "PATCH"]:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "DELETE":
        try:
            subject.delete()
        except Exception:
            return Response(
                {
                    "error": (
                        "This subject cannot be deleted "
                        "because other records may depend on it."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------
# -------------------------
# Academic Years API
# -------------------------

@api_view(["GET", "POST"])
@permission_classes([CanAccessAcademics])
def academic_year_list(request):
    if request.method == "GET":
        years = AcademicYear.objects.all().order_by("-start_date")
        serializer = AcademicYearSerializer(years, many=True)
        return Response(serializer.data)

    serializer = AcademicYearSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessAcademics])
def academic_year_detail(request, year_id):
    try:
        year = AcademicYear.objects.get(id=year_id)
    except AcademicYear.DoesNotExist:
        return Response(
            {"error": "Academic year not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = AcademicYearSerializer(year)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = AcademicYearSerializer(
            year,
            data=request.data,
        )

    elif request.method == "PATCH":
        serializer = AcademicYearSerializer(
            year,
            data=request.data,
            partial=True,
        )

    if request.method in ["PUT", "PATCH"]:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "DELETE":
        try:
            year.delete()
        except Exception:
            return Response(
                {
                    "error": (
                        "This academic year cannot be deleted "
                        "because other records may depend on it."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# -------------------------
# Close Academic Year
# -------------------------

@api_view(["POST"])
@permission_classes([CanAccessAcademics])
def close_academic_year(request, year_id):
    # Only Admin users can close an academic year.
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    ):
        return Response(
            {
                "error": (
                    "Only admins can close an academic year."
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Find the academic year.
    try:
        academic_year = AcademicYear.objects.get(
            id=year_id
        )
    except AcademicYear.DoesNotExist:
        return Response(
            {"error": "Academic year not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Prevent closing the same year twice.
    if academic_year.is_closed:
        return Response(
            {
                "error": (
                    "Academic year is already closed."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check whether this academic year still has
    # active student enrollments.
    has_active_enrollments = (
        StudentEnrollment.objects.filter(
            class_section__academic_year=academic_year,
            status=StudentEnrollment.Status.ACTIVE,
        ).exists()
    )

    # Do not close a year while students are still active.
    if has_active_enrollments:
        return Response(
            {
                "error": (
                    "Academic year cannot be closed while "
                    "it has active student enrollments."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Safely close the academic year.
    with transaction.atomic():
        academic_year.is_current = False
        academic_year.is_closed = True

        academic_year.save(
            update_fields=[
                "is_current",
                "is_closed",
            ]
        )

    return Response(
        {
            "message": (
                "Academic year closed successfully."
            ),
            "academic_year": {
                "id": academic_year.id,
                "name": academic_year.name,
                "is_current": academic_year.is_current,
                "is_closed": academic_year.is_closed,
            },
        },
        status=status.HTTP_200_OK,
    )

@api_view(["GET", "POST"])
@permission_classes([CanAccessAcademics])
def section_list(request):
    if request.method == "GET":
        sections = ClassSection.objects.select_related(
            "grade_level",
            "academic_year",
        )

        serializer = ClassSectionSerializer(sections, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ClassSectionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessAcademics])
def section_detail(request, section_id):
    try:
        section = ClassSection.objects.select_related(
            "academic_year",
            "grade_level",
        ).get(id=section_id)

    except ClassSection.DoesNotExist:
        return Response(
            {"error": "Class section not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # READ
    if request.method == "GET":
        serializer = ClassSectionSerializer(section)
        return Response(serializer.data)

    # FULL UPDATE
    elif request.method == "PUT":
        serializer = ClassSectionSerializer(
            section,
            data=request.data,
        )

    # PARTIAL UPDATE
    elif request.method == "PATCH":
        serializer = ClassSectionSerializer(
            section,
            data=request.data,
            partial=True,
        )

    # SAVE UPDATE
    if request.method in ["PUT", "PATCH"]:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE
    elif request.method == "DELETE":
        # Historical sections from a closed academic
        # year must not be deleted.
        if section.academic_year.is_closed:
            return Response(
                {
                    "error": (
                        "Class sections cannot be deleted "
                        "from a closed academic year."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            section.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                {
                    "error": (
                        "Cannot delete this section because "
                        "other records may depend on it."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
@api_view(["GET", "POST"])
@permission_classes([CanAccessAcademics])
def teaching_assignment_list(request):
    if request.method == "GET":
        assignments = TeachingAssignment.objects.select_related(
            "teacher",
            "subject",
            "class_section",
            "class_section__grade_level",
            "class_section__academic_year",
        )

        teacher_id = request.query_params.get("teacher")
        if teacher_id:
            assignments = assignments.filter(teacher_id=teacher_id)

        subject_id = request.query_params.get("subject")
        if subject_id:
            assignments = assignments.filter(subject_id=subject_id)

        section_id = request.query_params.get("section")
        if section_id:
            assignments = assignments.filter(
                class_section_id=section_id
            )

        serializer = TeachingAssignmentSerializer(
            assignments,
            many=True,
        )
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TeachingAssignmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessAcademics])
def teaching_assignment_detail(request, assignment_id):
    try:
        assignment = TeachingAssignment.objects.select_related(
            "class_section",
            "class_section__academic_year",
        ).get(id=assignment_id)

    except TeachingAssignment.DoesNotExist:
        return Response(
            {"error": "Teaching assignment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = TeachingAssignmentSerializer(assignment)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TeachingAssignmentSerializer(
            assignment,
            data=request.data,
        )

    elif request.method == "PATCH":
        serializer = TeachingAssignmentSerializer(
            assignment,
            data=request.data,
            partial=True,
        )

    if request.method in ["PUT", "PATCH"]:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif request.method == "DELETE":
        academic_year = assignment.class_section.academic_year

        if academic_year.is_closed:
            return Response(
                {
                    "error": (
                        "Teaching assignments cannot be deleted "
                        "from a closed academic year."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            assignment.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                {
                    "error": (
                        "Cannot delete this teaching assignment "
                        "because other records may depend on it."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

@api_view(["GET", "POST"])
@permission_classes([CanAccessResults])
def result_list(request):
    if request.method == "GET":
        results = Result.objects.all()

        # If the logged-in user is a Student,
        # only show that student's own results.
        if request.user.groups.filter(name="Student").exists():
            try:
                student_profile = request.user.student_profile
            except AttributeError:
                return Response(
                    {"error": "Student profile not found."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            results = results.filter(
                enrollment__student=student_profile
            )

        # Query parameter filters
        student = request.query_params.get("student")
        subject = request.query_params.get("subject")
        term = request.query_params.get("term")
        section = request.query_params.get("section")

        if student:
            results = results.filter(
                enrollment__student_id=student
            )

        if subject:
            results = results.filter(
                subject_id=subject
            )

        if term:
            results = results.filter(
                term=term
            )

        if section:
            results = results.filter(
                enrollment__class_section_id=section
            )

        serializer = ResultSerializer(
            results,
            many=True,
        )

        return Response(serializer.data)

    if request.method == "POST":
        serializer = ResultSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessResults])
def result_detail(request, result_id):
    try:
        result = (
            Result.objects
            .select_related(
                "enrollment",
                "enrollment__student",
                "enrollment__class_section",
                "enrollment__class_section__academic_year",
            )
            .get(id=result_id)
        )
    except Result.DoesNotExist:
        return Response(
            {"error": "Result not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Students can only access their own result.
    if request.user.groups.filter(name="Student").exists():
        try:
            student_profile = request.user.student_profile
        except AttributeError:
            return Response(
                {"error": "Student profile not found."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if result.enrollment.student != student_profile:
            return Response(
                {"error": "You cannot access this result."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # READ
    if request.method == "GET":
        serializer = ResultSerializer(result)
        return Response(serializer.data)

    # UPDATE
    if request.method in ["PUT", "PATCH"]:
        serializer = ResultSerializer(
            result,
            data=request.data,
            partial=request.method == "PATCH",
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE
    if request.method == "DELETE":
        academic_year = (
            result
            .enrollment
            .class_section
            .academic_year
        )

        # Historical results from a closed year
        # must not be deleted.
        if academic_year.is_closed:
            return Response(
                {
                    "error": (
                        "Results cannot be deleted "
                        "from a closed academic year."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# -------------------------
# Timetable API
# -------------------------

@api_view(["GET", "POST"])
@permission_classes([CanAccessAcademics])
def timetable_list(request):
    if request.method == "GET":
        timetables = Timetable.objects.select_related(
            "teaching_assignment",
            "teaching_assignment__teacher",
            "teaching_assignment__subject",
            "teaching_assignment__class_section",
            "teaching_assignment__class_section__grade_level",
            "teaching_assignment__class_section__academic_year",
        )

        # Filter by day
        day = request.query_params.get("day")
        if day:
            timetables = timetables.filter(
                day_of_week=day
            )

        # Filter by teacher
        teacher = request.query_params.get("teacher")
        if teacher:
            timetables = timetables.filter(
                teaching_assignment__teacher_id=teacher
            )

        # Filter by subject
        subject = request.query_params.get("subject")
        if subject:
            timetables = timetables.filter(
                teaching_assignment__subject_id=subject
            )

        # Filter by class section
        section = request.query_params.get("section")
        if section:
            timetables = timetables.filter(
                teaching_assignment__class_section_id=section
            )

        serializer = TimetableSerializer(
            timetables,
            many=True,
        )

        return Response(serializer.data)

    if request.method == "POST":
        serializer = TimetableSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessAcademics])
def timetable_detail(request, timetable_id):
    try:
        timetable = Timetable.objects.get(
            id=timetable_id
        )
    except Timetable.DoesNotExist:
        return Response(
            {"error": "Timetable not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = TimetableSerializer(timetable)
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = TimetableSerializer(
            timetable,
            data=request.data,
            partial=request.method == "PATCH",
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "DELETE":
        timetable.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


# -------------------------
## -------------------------
# Report Card API
# -------------------------

@api_view(["GET"])
@permission_classes([CanAccessResults])
def report_card(request, student_id):
    # Find the student.
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Students can only view their own report card.
    if request.user.groups.filter(name="Student").exists():
        try:
            student_profile = request.user.student_profile
        except AttributeError:
            return Response(
                {"error": "Student profile not found."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if student.id != student_profile.id:
            return Response(
                {
                    "error": (
                        "You cannot access another student's "
                        "report card."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    # Get enrollment ID from query parameter if provided.
    #
    # Example:
    # /api/academics/report-cards/1/?enrollment=1
    enrollment_id = request.query_params.get("enrollment")

    # Get all enrollments belonging to this student.
    enrollments = (
        StudentEnrollment.objects
        .select_related(
            "class_section",
            "class_section__grade_level",
            "class_section__academic_year",
        )
        .filter(student=student)
    )

    # If an enrollment ID was provided,
    # use that specific enrollment.
    if enrollment_id:
        try:
            enrollment = enrollments.get(id=enrollment_id)
        except StudentEnrollment.DoesNotExist:
            return Response(
                {
                    "error": (
                        "Enrollment not found for this student."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    # Otherwise use the student's latest enrollment.
    else:
        enrollment = (
            enrollments
            .order_by("-enrollment_date", "-id")
            .first()
        )

        if enrollment is None:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    # Get results belonging to the selected enrollment.
    results = (
        Result.objects
        .filter(enrollment=enrollment)
        .select_related("subject")
        .order_by("subject__name", "term")
    )

    subjects = {}

    # Organize results by subject.
    for result in results:
        subject_id = result.subject.id

        if subject_id not in subjects:
            subjects[subject_id] = {
                "subject_id": subject_id,
                "subject_name": result.subject.name,
                "term_1": None,
                "term_2": None,
                "average": None,
            }

        subjects[subject_id][result.term] = float(
            result.score
        )

    # Calculate the average for each subject.
    for subject_data in subjects.values():
        scores = []

        if subject_data["term_1"] is not None:
            scores.append(subject_data["term_1"])

        if subject_data["term_2"] is not None:
            scores.append(subject_data["term_2"])

        if scores:
            subject_data["average"] = round(
                sum(scores) / len(scores),
                2,
            )

    # Calculate overall average.
    subject_averages = [
        subject["average"]
        for subject in subjects.values()
        if subject["average"] is not None
    ]

    overall_average = None

    if subject_averages:
        overall_average = round(
            sum(subject_averages)
            / len(subject_averages),
            2,
        )

    # Return the complete report card.
    return Response({
        "student": {
            "id": student.id,
            "student_id": student.student_id,
            "name": (
                f"{student.first_name} "
                f"{student.last_name}"
            ),
        },

        "enrollment": {
            "id": enrollment.id,
            "status": enrollment.status,
        },

        "academic_year": (
            enrollment.class_section.academic_year.name
        ),

        "grade": (
            enrollment.class_section.grade_level.number
        ),

        "section": enrollment.class_section.name,

        "subjects": list(subjects.values()),

        "overall_average": overall_average,
    })


@api_view(["POST"])
@permission_classes([CanAccessAcademics])
def start_academic_year(request, year_id):
    # Only Admin users can start an academic year.
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    ):
        return Response(
            {
                "error": (
                    "Only admins can start an academic year."
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Find the academic year.
    try:
        academic_year = AcademicYear.objects.get(
            id=year_id
        )
    except AcademicYear.DoesNotExist:
        return Response(
            {"error": "Academic year not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Closed years cannot be started again.
    if academic_year.is_closed:
        return Response(
            {
                "error": (
                    "A closed academic year cannot be started."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Prevent starting the same year twice.
    if academic_year.is_current:
        return Response(
            {
                "error": (
                    "Academic year is already current."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Only one academic year can be current.
    if AcademicYear.objects.filter(
        is_current=True
    ).exists():
        return Response(
            {
                "error": (
                    "Another academic year is already current."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    academic_year.is_current = True
    academic_year.save(
        update_fields=["is_current"]
    )

    return Response(
        {
            "message": (
                "Academic year started successfully."
            ),
            "academic_year": {
                "id": academic_year.id,
                "name": academic_year.name,
                "is_current": academic_year.is_current,
                "is_closed": academic_year.is_closed,
            },
        },
        status=status.HTTP_200_OK,
    )