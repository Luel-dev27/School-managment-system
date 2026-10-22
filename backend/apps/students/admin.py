from django.contrib import admin

from .models import Student, StudentEnrollment, Attendance

admin.site.register(Student)
admin.site.register(StudentEnrollment)
admin.site.register(Attendance)