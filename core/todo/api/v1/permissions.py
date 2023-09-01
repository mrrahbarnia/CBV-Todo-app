from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # ============= Object-level permission to only allow users of an object to edit or delete it ============= # 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id