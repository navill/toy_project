from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'You do not have permission of this object.'

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS: GET, OPTIONS, HEAD
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAdminUserOrReadOnly(BasePermission):
    message = "Allows edit only to admin users, if not read only"

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        else:
            if request.method in SAFE_METHODS:
                return True
            else:
                return False


class IsOwner(BasePermission):
    message = 'You do not have permission of this object.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
