from django.contrib import admin
from .models import AcademicYear, ClassSection, GradeLevel, Subject, TeachingAssignment, Result, Timetable

admin.site.register(AcademicYear)
admin.site.register(GradeLevel)
admin.site.register(Subject)
admin.site.register(ClassSection)
admin.site.register(Timetable)
admin.site.register(Result)
admin.site.register(TeachingAssignment)