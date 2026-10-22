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