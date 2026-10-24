from django.urls import path
from .views import (
    graduate_student,
    student_list, 
    student_detail,
    enrollment_list,
    enrollment_detail,
    attendance_list,
    attendance_detail,
    promote_student,
    transfer_student,
    repeat_grade,
)

urlpatterns = [
    path("", student_list, name="student-list"),
    path("<int:student_id>/", student_detail, name="student-detail"),
    path("enrollments/", enrollment_list, name="enrollment-list"),
    path("enrollments/<int:enrollment_id>/", enrollment_detail, name="enrollment-detail"),
    path("attendance/", attendance_list, name="attendance-list"),
    path("attendance/<int:attendance_id>/", attendance_detail, name="attendance-detail"),
   
   path(
    "<int:student_id>/promote/",
    promote_student,
    name="promote-student",
    ),

    path(
    "<int:student_id>/graduate/",
    graduate_student,
    name="graduate-student",
    ),

    path(
    "<int:student_id>/transfer/",
    transfer_student,
    name="transfer-student",
   ),

   path(
    "<int:student_id>/repeat/",
    repeat_grade,
    name="repeat-grade",
   ),
]