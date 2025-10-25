from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the admin user.
        return request.user and request.user.is_staff


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    Extends DjangoModelPermissions to include 'view' permissions.
    """

    def __init__(self):
        super().__init__()
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
        self.perms_map["OPTIONS"] = ["%(app_label)s.view_%(model_name)s"]
        self.perms_map["HEAD"] = ["%(app_label)s.view_%(model_name)s"]


class ViewCustomerHistoryPermission(permissions.BasePermission):
    """
    Custom permission to allow only staff users to view customer history.
    """

    def has_permission(self, request, view):
        return request.user.has_perm("store.view_history")
