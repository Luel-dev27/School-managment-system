from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsTeacherOrAdmin


from .models import Student, StudentEnrollment, Attendance
from .serializers import StudentSerializer, StudentEnrollmentSerializer, AttendanceSerializer

    
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def student_list(request):

    # READ: Get all students    
    if request.method == "GET":
        students = Student.objects.all()

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
@permission_classes([IsAuthenticated])
def student_detail(request, student_id):

    # Find the student by database ID
    try:
        student = Student.objects.get(id=student_id)

    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # READ: Get one student's information
    if request.method == "GET":
        serializer = StudentSerializer(student)

        return Response(serializer.data)

    # UPDATE: Replace the student's submitted information
    elif request.method == "PUT":
        serializer = StudentSerializer(
            student,
            data=request.data,
        )

    # PARTIAL UPDATE: Change only the submitted fields
    elif request.method == "PATCH":
        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True,
        )

    # Save the updated information
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
def enrollment_list(request):
    if request.method == "GET":
        enrollments = StudentEnrollment.objects.select_related(
            "student",
            "class_section",
            "class_section__grade_level",
            "class_section__academic_year",
        )

        student_id = request.query_params.get("student")
        if student_id:
            enrollments = enrollments.filter(student_id=student_id)

        section_id = request.query_params.get("section")
        if section_id:
            enrollments = enrollments.filter(
                class_section_id=section_id
            )

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

    elif request.method == "POST":
        serializer = StudentEnrollmentSerializer(data=request.data)

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
def enrollment_detail(request, enrollment_id):
    try:
        enrollment = StudentEnrollment.objects.get(
            id=enrollment_id
        )
    except StudentEnrollment.DoesNotExist:
        return Response(
            {"error": "Enrollment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = StudentEnrollmentSerializer(enrollment)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = StudentEnrollmentSerializer(
            enrollment,
            data=request.data,
        )

    elif request.method == "PATCH":
        serializer = StudentEnrollmentSerializer(
            enrollment,
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
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsTeacherOrAdmin])
def attendance_list(request):
    if request.method == "GET":
        attendance_records = Attendance.objects.all()

        date = request.query_params.get("date")
        status_value = request.query_params.get("status")
        student = request.query_params.get("student")
        section = request.query_params.get("section")

        if date:
            attendance_records = attendance_records.filter(date=date)

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

    if request.method == "POST":
        serializer = AttendanceSerializer(data=request.data)

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
@permission_classes([IsTeacherOrAdmin])
def attendance_detail(request, attendance_id):
    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return Response(
            {"error": "Attendance record not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

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

    if request.method == "DELETE":
        attendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)