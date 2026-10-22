from django.urls import path
from .views import (
    grade_list,
    grade_detail,
    subject_list,
    subject_detail,
    academic_year_list,
    academic_year_detail,
    section_list,
    section_detail,
    teaching_assignment_list,
    teaching_assignment_detail,
    result_list,
    result_detail
)


urlpatterns = [
    # Grade levels
    path("grades/", grade_list, name="grade-list"),
    path(
        "grades/<int:grade_id>/",
        grade_detail,
        name="grade-detail",
    ),

    # Subjects
    path("subjects/", subject_list, name="subject-list"),
    path(
        "subjects/<int:subject_id>/",
        subject_detail,
        name="subject-detail",
    ),

    # Academic years
    path("years/", academic_year_list, name="academic-year-list"),
    path(
        "years/<int:year_id>/",
        academic_year_detail,
        name="academic-year-detail",
    ),
    # Sections
    path("sections/", section_list, name="section-list"),
    path(
    "sections/<int:section_id>/",
    section_detail,
    name="section-detail",
    ),
    # Teaching Assignments
    path(
    "teaching-assignments/",
    teaching_assignment_list,
    name="teaching-assignment-list",
    ),
    path(
    "teaching-assignments/<int:assignment_id>/",
    teaching_assignment_detail,
    name="teaching-assignment-detail",
    ),

    # Results
    path("results/", result_list, name="result-list"),
    path("results/<int:result_id>/", result_detail, name="result-detail"),
]
