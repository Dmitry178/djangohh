from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AuthReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return False


# class IsAuthor(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             return request.user.is_author
#         return False
