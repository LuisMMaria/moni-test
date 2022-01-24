from rest_framework.permissions import IsAdminUser, BasePermission

# Import User model
from users.models import User


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsStaffUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user == User.objects.get(pk=view.kwargs['pk'])
