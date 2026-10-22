from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/students/", include("apps.students.urls")),
    path("api/teachers/", include("apps.teachers.urls")),
    path("api/academics/", include("apps.academics.urls")),
    path("api/accounts/", include("apps.accounts.urls")),
]
