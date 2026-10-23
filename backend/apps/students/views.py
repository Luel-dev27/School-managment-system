from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.permissions import CanAccessAttendance, IsTeacherOrAdmin, CanAccessStudents, CanAccessEnrollments


from .models import Student, StudentEnrollment, Attendance
from .serializers import StudentSerializer, StudentEnrollmentSerializer, AttendanceSerializer

    
@api_view(["GET", "POST"])
@permission_classes([CanAccessStudents])
def student_list(request):

    # READ: Get all students    
    if request.method == "GET":
        students = Student.objects.all()
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


        # SEARCH: By first name, last name, or school student ID
        search = request.query_params.get("search")

        if search:
            students = students.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(student_id__icontains=search)
            )

        # FILTER: By the school's student ID
        student_id = request.query_params.get("student_id")

        if student_id:
            students = students.filter(student_id=student_id)

        # FILTER: By grade number, such as Grade 9 or Grade 10
        grade = request.query_params.get("grade")

        if grade:
            students = students.filter(
                grade_level__number=grade
            )

        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)

    # CREATE: Register a new student
    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)

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