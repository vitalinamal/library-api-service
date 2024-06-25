from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a payment or admins to view it.
    """

    def has_object_permission(self, request, view, obj):
        return ((request.user and request.user.is_staff)
                or obj.borrowing_id.user == request.user)
