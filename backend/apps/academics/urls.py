from django.urls import path

from .views import (
    close_academic_year,
    grade_list,
    grade_detail,
    start_academic_year,
    subject_list,
    subject_detail,
    academic_year_list,
    academic_year_detail,
    section_list,
    section_detail,
    teaching_assignment_list,
    teaching_assignment_detail,
    result_list,
    result_detail,
    timetable_list,
    timetable_detail,
    report_card
)


urlpatterns = [
    # Grade levels
    path(
        "grades/",
        grade_list,
        name="grade-list",
    ),
    path(
        "grades/<int:grade_id>/",
        grade_detail,
        name="grade-detail",
    ),

    # Subjects
    path(
        "subjects/",
        subject_list,
        name="subject-list",
    ),
    path(
        "subjects/<int:subject_id>/",
        subject_detail,
        name="subject-detail",
    ),

    # Academic years
    path(
        "years/",
        academic_year_list,
        name="academic-year-list",
    ),
    path(
        "years/<int:year_id>/",
        academic_year_detail,
        name="academic-year-detail",
    ),

    # Class sections
    path(
        "sections/",
        section_list,
        name="section-list",
    ),
    path(
        "sections/<int:section_id>/",
        section_detail,
        name="section-detail",
    ),

    # Teaching assignments
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
    path(
        "results/",
        result_list,
        name="result-list",
    ),
    path(
        "results/<int:result_id>/",
        result_detail,
        name="result-detail",
    ),

    # Timetables
    path(
        "timetables/",
        timetable_list,
        name="timetable-list",
    ),
    path(
        "timetables/<int:timetable_id>/",
        timetable_detail,
        name="timetable-detail",
    ),

     # Report cards
    path(
        "report-cards/<int:student_id>/",
        report_card,
        name="report-card",
    ),

    path(
    "years/<int:year_id>/close/",
    close_academic_year,
    name="close-academic-year",
    ),
    path(
    "years/<int:year_id>/start/",
    start_academic_year,
    name="start-academic-year",
   ),
]