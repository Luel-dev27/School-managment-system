from rest_framework.permissions import BasePermission


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.user.groups.filter(
            name__in=["Teacher", "Admin"]
        ).exists()

class CanAccessResults(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(
            name__in=["Teacher", "Admin"]
        ).exists():
            return True

        if (
            request.method == "GET"
            and request.user.groups.filter(name="Student").exists()
        ):
            return True

        return False


class CanAccessStudents(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Admin group can do everything
        if request.user.groups.filter(name="Admin").exists():
            return True

        # Teachers and Students can only read
        if (
            request.method == "GET"
            and request.user.groups.filter(
                name__in=["Teacher", "Student"]
            ).exists()
        ):
            return True

        return False


class CanAccessEnrollments(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name="Admin").exists():
            return True

        if (
            request.method == "GET"
            and request.user.groups.filter(
                name__in=["Teacher", "Student"]
            ).exists()
        ):
            return True

        return False


class CanAccessAttendance(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(
            name__in=["Teacher", "Admin"]
        ).exists():
            return True

        if (
            request.method == "GET"
            and request.user.groups.filter(
                name="Student"
            ).exists()
        ):
            return True

        return False
    

class CanAccessTeachers(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Admin can manage teachers
        if request.user.groups.filter(name="Admin").exists():
            return True

        # Teachers and Students can only view
        if (
            request.method == "GET"
            and request.user.groups.filter(
                name__in=["Teacher", "Student"]
            ).exists()
        ):
            return True

        return False

class CanAccessAcademics(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Admin can manage academic data
        if request.user.groups.filter(name="Admin").exists():
            return True

        # Teachers and Students can only view academic data
        if (
            request.method == "GET"
            and request.user.groups.filter(
                name__in=["Teacher", "Student"]
            ).exists()
        ):
            return True

        return False