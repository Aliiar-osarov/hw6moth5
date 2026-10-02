from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    ## Разрешение GET для всех пользователей 
    ## редактировать удалять обьект только владельцу и админу
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and (
                obj.user == request.user or request.user.is_staff
            )
        )

class IsAdminOrReadOnly(permissions.BasePermission):
    ## методы POST PUT DELETE только для администраторов 
    ## всем остальным кроме администраторов можно только SafeMethod тоесть GET
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    