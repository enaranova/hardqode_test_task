from rest_framework import permissions

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.qroups.filter(name='Professors').exists()

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Students').exists()