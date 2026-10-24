from django.db.models import Q
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.permissions import CanAccessAttendance, CanAccessStudents, CanAccessEnrollments

from apps.academics.models import ClassSection
from .models import Student, StudentEnrollment, Attendance
from .serializers import StudentSerializer, StudentEnrollmentSerializer, AttendanceSerializer

    
@api_view(["GET", "POST"])
@permission_classes([CanAccessStudents])
def student_list(request):

    # READ: Get students
    if request.method == "GET":
        students = Student.objects.all()

        # Student users can only see their own profile.
        if request.user.groups.filter(name="Student").exists():
            try:
                student_profile = request.user.student_profile
            except AttributeError:
                return Response(
                    {"error": "Student profile not found."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            students = students.filter(
                id=student_profile.id
            )

        # SEARCH: By first name, last name, or student ID
        search = request.query_params.get("search")

        if search:
            students = students.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(student_id__icontains=search)
            )

        # FILTER: By school student ID
        student_id = request.query_params.get("student_id")

        if student_id:
            students = students.filter(
                student_id=student_id
            )

        # FILTER: By grade number
        grade = request.query_params.get("grade")

        if grade:
            students = students.filter(
                grade_level__number=grade
            )

        serializer = StudentSerializer(
            students,
            many=True,
        )

        return Response(serializer.data)

    # CREATE: Register a new student
    elif request.method == "POST":
        serializer = StudentSerializer(
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

# READ one student, UPDATE a student, or DELETE a student
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([CanAccessStudents])
def student_detail(request, student_id):

    # Find the student by database ID
    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # SECURITY:
    # A logged-in Student can only access their own profile.
    if request.user.groups.filter(name="Student").exists():
        try:
            student_profile = request.user.student_profile

        except AttributeError:
            return Response(
                {"error": "Student profile not found."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Block access if this is another student's profile
        if student.id != student_profile.id:
            return Response(
                {"error": "You cannot access this student."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # READ: Get one student's information
    if request.method == "GET":
        serializer = StudentSerializer(student)

        return Response(serializer.data)

    # UPDATE: Replace all submitted student information
    elif request.method == "PUT":
        serializer = StudentSerializer(
            student,
            data=request.data,
        )

    # PARTIAL UPDATE: Change only submitted fields
    elif request.method == "PATCH":
        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True,
        )

    # Save PUT or PATCH changes
    if request.method in ["PUT", "PATCH"]:
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE: Remove the student
    elif request.method == "DELETE":
        student.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

@api_view(["GET", "POST"])
@permission_classes([CanAccessEnrollments])
def enrollment_list(request):
    if request.method == "GET":
        enrollments = StudentEnrollment.objects.select_related(
            "student",
            "class_section",
            "class_section__grade_level",
            "class_section__academic_year",
        )

        # SECURITY:
        # Students can only see their own enrollments.
        if request.user.groups.filter(name="Student").exists():
            try:
                student_profile = request.user.student_profile
            except AttributeError:
                return Response(
                    {"error": "Student profile not found."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            enrollments = enrollments.filter(
                student=student_profile
            )

        # FILTER: By student database ID
        student_id = request.query_params.get("student")

        if student_id:
            enrollments = enrollments.filter(
                student_id=student_id
            )

        # FILTER: By class section
        section_id = request.query_params.get("section")

        if section_id:
            enrollments = enrollments.filter(
                class_section_id=section_id
            )

        # FILTER: By enrollment status
        enrollment_status = request.query_params.get("status")

        if enrollment_status:
            enrollments = enrollments.filter(
                status=enrollment_status
            )

        serializer = StudentEnrollmentSerializer(
            enrollments,
            many=True,
        )

        return Response(serializer.data)

    # CREATE
    elif request.method == "POST":
        serializer = StudentEnrollmentSerializer(
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
@permission_classes([CanAccessEnrollments])
def enrollment_detail(request, enrollment_id):
    try:
        enrollment = StudentEnrollment.objects.select_related(
            "student",
            "class_section",
        ).get(
            id=enrollment_id
        )

    except StudentEnrollment.DoesNotExist:
        return Response(
            {"error": "Enrollment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # SECURITY:
    # A Student can only access their own enrollment.
    if request.user.groups.filter(name="Student").exists():
        try:
            student_profile = request.user.student_profile
        except AttributeError:
            return Response(
                {"error": "Student profile not found."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if enrollment.student != student_profile:
            return Response(
                {"error": "You cannot access this enrollment."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # READ
    if request.method == "GET":
        serializer = StudentEnrollmentSerializer(
            enrollment
        )

        return Response(serializer.data)

    # FULL UPDATE
    elif request.method == "PUT":
        serializer = StudentEnrollmentSerializer(
            enrollment,
            data=request.data,
        )

    # PARTIAL UPDATE
    elif request.method == "PATCH":
        serializer = StudentEnrollmentSerializer(
            enrollment,
            data=request.data,
            partial=True,
        )

    # SAVE PUT/PATCH
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
        enrollment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "POST"])
@permission_classes([CanAccessAttendance])
def attendance_list(request):
    if request.method == "GET":
        attendance_records = Attendance.objects.all()

        # SECURITY:
        # Students can only see their own attendance records.
        if request.user.groups.filter(name="Student").exists():
            try:
                student_profile = request.user.student_profile
            except AttributeError:
                return Response(
                    {"error": "Student profile not found."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            attendance_records = attendance_records.filter(
                enrollment__student=student_profile
            )

        # FILTERS
        date = request.query_params.get("date")
        status_value = request.query_params.get("status")
        student = request.query_params.get("student")
        section = request.query_params.get("section")

        if date:
            attendance_records = attendance_records.filter(
                date=date
            )

        if status_value:
            attendance_records = attendance_records.filter(
                status=status_value
            )

        if student:
            attendance_records = attendance_records.filter(
                enrollment__student_id=student
            )

        if section:
            attendance_records = attendance_records.filter(
                enrollment__class_section_id=section
            )

        serializer = AttendanceSerializer(
            attendance_records,
            many=True,
        )

        return Response(serializer.data)

    # CREATE ATTENDANCE
    if request.method == "POST":
        serializer = AttendanceSerializer(
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
@permission_classes([CanAccessAttendance])
def attendance_detail(request, attendance_id):
    try:
        attendance = Attendance.objects.select_related(
            "enrollment",
            "enrollment__student",
        ).get(
            id=attendance_id
        )

    except Attendance.DoesNotExist:
        return Response(
            {"error": "Attendance record not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # SECURITY:
    # A Student can only access their own attendance record.
    if request.user.groups.filter(name="Student").exists():
        try:
            student_profile = request.user.student_profile
        except AttributeError:
            return Response(
                {"error": "Student profile not found."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if attendance.enrollment.student != student_profile:
            return Response(
                {
                    "error":
                    "You cannot access this attendance record."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    # READ
    if request.method == "GET":
        serializer = AttendanceSerializer(attendance)

        return Response(serializer.data)

    # UPDATE
    if request.method in ["PUT", "PATCH"]:
        serializer = AttendanceSerializer(
            attendance,
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
        attendance.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

@api_view(["POST"])
@permission_classes([CanAccessStudents])
def promote_student(request, student_id):
    # Only Admin users can promote students.
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    ):
        return Response(
            {"error": "Only admins can promote students."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Find the student.
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Get destination class section.
    class_section_id = request.data.get("class_section")

    if not class_section_id:
        return Response(
            {"error": "class_section is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        new_section = ClassSection.objects.select_related(
            "grade_level",
            "academic_year",
        ).get(id=class_section_id)
    except ClassSection.DoesNotExist:
        return Response(
            {"error": "Class section not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Find the student's latest enrollment.
    current_enrollment = (
        StudentEnrollment.objects
        .select_related(
            "class_section",
            "class_section__grade_level",
            "class_section__academic_year",
        )
        .filter(student=student)
        .order_by("-enrollment_date", "-id")
        .first()
    )

    if current_enrollment is None:
        return Response(
            {"error": "Student has no enrollment."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Students in a final grade must graduate,
    # not be promoted to another grade.
    if current_enrollment.class_section.grade_level.is_final_grade:
        return Response(
            {
                "error": (
                    "Students in the final grade should "
                    "be graduated, not promoted."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_grade = current_enrollment.class_section.grade_level.number
    new_grade = new_section.grade_level.number

    # The destination must be exactly one grade higher.
    if new_grade != old_grade + 1:
        return Response(
            {
                "error": (
                    f"Student can only be promoted from "
                    f"Grade {old_grade} to Grade {old_grade + 1}."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Destination must belong to a later academic year.
    current_year = (
        current_enrollment.class_section.academic_year
    )

    new_year = new_section.academic_year

    if new_year.start_date <= current_year.start_date:
        return Response(
            {
                "error": (
                    "Promotion must be to a later "
                    "academic year."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Prevent duplicate enrollment in the destination section.
    if StudentEnrollment.objects.filter(
        student=student,
        class_section=new_section,
    ).exists():
        return Response(
            {
                "error": (
                    "Student is already enrolled in "
                    "this class section."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Complete the old enrollment and create the new
    # enrollment as one database transaction.
    with transaction.atomic():
        current_enrollment.status = (
            StudentEnrollment.Status.COMPLETED
        )
        current_enrollment.save()

        new_enrollment = StudentEnrollment.objects.create(
            student=student,
            class_section=new_section,
            status=StudentEnrollment.Status.ACTIVE,
        )

        # Keep the student's current grade synchronized.
        student.grade_level = new_section.grade_level
        student.save(update_fields=["grade_level"])

    return Response(
        {
            "message": "Student promoted successfully.",
            "student": {
                "id": student.id,
                "student_id": student.student_id,
                "name": (
                    f"{student.first_name} "
                    f"{student.last_name}"
                ),
            },
            "previous_enrollment": {
                "id": current_enrollment.id,
                "grade": old_grade,
                "section": (
                    current_enrollment.class_section.name
                ),
                "academic_year": (
                    current_enrollment
                    .class_section
                    .academic_year
                    .name
                ),
                "status": current_enrollment.status,
            },
            "new_enrollment": {
                "id": new_enrollment.id,
                "grade": new_grade,
                "section": new_section.name,
                "academic_year": new_section.academic_year.name,
                "status": new_enrollment.status,
            },
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@permission_classes([CanAccessStudents])
def graduate_student(request, student_id):
    # Only Admin users can graduate students.
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name="Admin").exists()
    ):
        return Response(
            {"error": "Only admins can graduate students."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if student.status == Student.Status.GRADUATED:
        return Response(
            {"error": "Student is already graduated."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    current_enrollment = (
        StudentEnrollment.objects
        .select_related(
            "class_section",
            "class_section__grade_level",
            "class_section__academic_year",
        )
        .filter(
            student=student,
            status=StudentEnrollment.Status.ACTIVE,
        )
        .first()
    )

    if current_enrollment is None:
        return Response(
            {"error": "Student has no active enrollment."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    grade_level = current_enrollment.class_section.grade_level

    if not grade_level.is_final_grade:
        return Response(
            {
                "error": (
                    "Student can only graduate from "
                    "a final grade."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        current_enrollment.status = (
            StudentEnrollment.Status.COMPLETED
        )
        current_enrollment.save()

        student.status = Student.Status.GRADUATED
        student.save()

    return Response({
        "message": "Student graduated successfully.",
        "student": {
            "id": student.id,
            "student_id": student.student_id,
            "name": (
                f"{student.first_name} "
                f"{student.last_name}"
            ),
            "status": student.status,
        },
        "final_enrollment": {
            "id": current_enrollment.id,
            "grade": grade_level.number,
            "section": current_enrollment.class_section.name,
            "academic_year": (
                current_enrollment
                .class_section
                .academic_year
                .name
            ),
            "status": current_enrollment.status,
        },
    })