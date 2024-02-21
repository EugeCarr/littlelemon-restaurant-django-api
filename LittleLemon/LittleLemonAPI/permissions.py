from rest_framework import permissions
from django.contrib.auth.models import Group

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return Group.objects.get(name="Manager").user_set.filter(id=request.user.id).exists()
        
class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return Group.objects.get(name="Delivery Crew").user_set.filter(id=request.user.id).exists()
    
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return not (
            Group.objects.get(name="Manager").user_set.filter(id=request.user.id).exists() or 
            Group.objects.get(name="Delivery Crew").user_set.filter(id=request.user.id).exists()
        )