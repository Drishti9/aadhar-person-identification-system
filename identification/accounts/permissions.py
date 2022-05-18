from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

# class IsAuthenticatedAndReadOnly(BasePermission):

#     def has_permission(self, request, view):
#         if (request.method in SAFE_METHODS and
#             request.user.is_authenticated):
#             return True
#         return False

class AllowPermission(BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_authenticated and (request.user.is_manager  or request.method in SAFE_METHODS)):
            return True
        return False


