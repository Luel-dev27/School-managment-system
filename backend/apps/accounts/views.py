from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.students.models import Student, StudentEnrollment
from apps.teachers.models import Teacher
from apps.academics.models import (
    Subject,
    ClassSection,
    TeachingAssignment,
)


# -------------------------
# Login API
# -------------------------

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(
        username=username,
        password=password,
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, created = Token.objects.get_or_create(
        user=user
    )

    groups = list(
        user.groups.values_list(
            "name",
            flat=True,
        )
    )

    return Response({
        "token": token.key,
        "username": user.username,
        "groups": groups,
    })


# -------------------------
# Dashboard API
# -------------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user

    # -------------------------
    # Admin Dashboard
    # -------------------------
    if (
        user.is_superuser
        or user.groups.filter(name="Admin").exists()
    ):
        data = {
            "role": "Admin",

            "summary": {
                "total_students": (
                    Student.objects.count()
                ),

                "total_teachers": (
                    Teacher.objects.count()
                ),

                "total_subjects": (
                    Subject.objects.count()
                ),

                "total_sections": (
                    ClassSection.objects.count()
                ),

                "active_enrollments": (
                    StudentEnrollment.objects.filter(
                        status=(
                            StudentEnrollment
                            .Status
                            .ACTIVE
                        )
                    ).count()
                ),
            },
        }

        return Response(data)

    # -------------------------
    # Teacher Dashboard
    # -------------------------
    if user.groups.filter(name="Teacher").exists():
        try:
            teacher = user.teacher_profile
        except AttributeError:
            return Response(
                {
                    "role": "Teacher",
                    "error": (
                        "Teacher profile not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        assignments = (
            TeachingAssignment.objects
            .filter(teacher=teacher)
            .select_related(
                "subject",
                "class_section",
                "class_section__grade_level",
                "class_section__academic_year",
            )
        )

        assignment_data = []

        for assignment in assignments:
            assignment_data.append({
                "assignment_id": assignment.id,

                "subject": (
                    assignment.subject.name
                ),

                "grade": (
                    assignment
                    .class_section
                    .grade_level
                    .number
                ),

                "section": (
                    assignment.class_section.name
                ),

                "academic_year": (
                    assignment
                    .class_section
                    .academic_year
                    .name
                ),
            })

        return Response({
            "role": "Teacher",

            "teacher": {
                "id": teacher.id,

                "teacher_id": (
                    teacher.teacher_id
                ),

                "name": (
                    f"{teacher.first_name} "
                    f"{teacher.last_name}"
                ),
            },

            "summary": {
                "total_assignments": (
                    assignments.count()
                ),
            },

            "teaching_assignments": (
                assignment_data
            ),
        })

    # -------------------------
    # Student Dashboard
    # -------------------------
    if user.groups.filter(name="Student").exists():
        try:
           student = user.student_profile
        except AttributeError:
            return Response(
                {
                    "role": "Student",
                    "error": "Student profile not found.",
               },
               status=status.HTTP_404_NOT_FOUND,
           )

        enrollment = (
            StudentEnrollment.objects
            .filter(
                student=student,
                status=StudentEnrollment.Status.ACTIVE,
            )
            .select_related(
                "class_section",
                "class_section__grade_level",
                "class_section__academic_year",
           )
           .first()
        )

        student_data = {
            "role": "Student",

            "student": {
                "id": student.id,
                "student_id": student.student_id,
                "name": (
                    f"{student.first_name} "
                    f"{student.last_name}"
               ),
           },

           "current_enrollment": None,
       }

        if enrollment:
            student_data["current_enrollment"] = {
                "enrollment_id": enrollment.id,

                "grade": (
                    enrollment
                    .class_section
                    .grade_level
                    .number
               ),

                "section": (
                    enrollment.class_section.name
               ),

                "academic_year": (
                    enrollment
                    .class_section
                    .academic_year
                    .name
                ),

                "status": enrollment.status,
        }

    return Response(student_data)

    # -------------------------
    # Unknown Role
    # -------------------------
    return Response({
        "role": "Unknown",
        "message": (
            "No dashboard is available for this user."
        ),
    })