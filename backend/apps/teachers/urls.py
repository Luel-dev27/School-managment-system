from django.urls import path
from .views import teacher_list, teacher_detail

urlpatterns = [
    path("", teacher_list, name="teacher-list"),
    path("<int:teacher_id>/", teacher_detail, name="teacher-detail"),
]