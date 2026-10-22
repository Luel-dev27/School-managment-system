from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Teacher
from .serializers import TeacherSerializer


@api_view(["GET", "POST"])
def teacher_list(request):

    # Retrieve teachers with optional search and filtering
    if request.method == "GET":
        teachers = Teacher.objects.all()

        # Search by first name, last name, or teacher ID
        search = request.query_params.get("search")

        if search:
            teachers = teachers.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(teacher_id__icontains=search)
            )

        # Filter by subject database ID
        subject_id = request.query_params.get("subject")

        if subject_id:
            teachers = teachers.filter(
                subjects__id=subject_id
            ).distinct()

        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    # Create a new teacher
    elif request.method == "POST":
        serializer = TeacherSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def teacher_detail(request, teacher_id):

    # Find the teacher using their database ID
    try:
        teacher = Teacher.objects.get(id=teacher_id)

    except Teacher.DoesNotExist:
        return Response(
            {"error": "Teacher not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Retrieve one teacher
    if request.method == "GET":
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    # Replace the teacher's editable data
    elif request.method == "PUT":
        serializer = TeacherSerializer(
            teacher,
            data=request.data
        )

    # Update only selected fields
    elif request.method == "PATCH":
        serializer = TeacherSerializer(
            teacher,
            data=request.data,
            partial=True
        )

    if request.method in ["PUT", "PATCH"]:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete the teacher
    elif request.method == "DELETE":
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)