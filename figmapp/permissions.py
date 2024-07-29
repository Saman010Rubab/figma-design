# permissions.py
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 1

class IsPublisher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in [1, 2]

class IsAdvertiser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in [1, 3]
        
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is trying to access their own profile
        return obj.user == request.user