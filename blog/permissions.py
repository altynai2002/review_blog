from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Only person who assigned has permission
    """

    def has_object_permission(self, request, view, obj):
        # check if user is object owner
        if obj.author == request.user:
            return True
        else:
            return False