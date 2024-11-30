from rest_framework import permissions

class IsFarmerOwner(permissions.BasePermission):
    def has_permission(self, request):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.farm_id.farmer_id == request.user
