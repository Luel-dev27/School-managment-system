from django.urls import path
from .views import (
    student_list, 
    student_detail,
    enrollment_list,
    enrollment_detail,
    attendance_list,
    attendance_detail,
)

urlpatterns = [
    path("", student_list, name="student-list"),
    path("<int:student_id>/", student_detail, name="student-detail"),
    path("enrollments/", enrollment_list, name="enrollment-list"),
    path("enrollments/<int:enrollment_id>/", enrollment_detail, name="enrollment-detail"),
    path("attendance/", attendance_list, name="attendance-list"),
    path("attendance/<int:attendance_id>/", attendance_detail, name="attendance-detail"),
]