
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # If obj has an attribute 'user', compare that user to the request user.
        owner = getattr(obj, 'user', obj)
        return request.user and owner == request.user