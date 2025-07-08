# api/permissions.py
from rest_framework import permissions

class IsMaestro(permissions.BasePermission):
    def has_permission(self, request, view):
        # O utilizador tem de estar autenticado E pertencer ao grupo "Maestros"
        return request.user.groups.filter(name='Maestros').exists()
