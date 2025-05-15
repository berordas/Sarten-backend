from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Permite lectura a cualquiera, pero solo permite escritura (POST, PUT, DELETE)
    a usuarios administradores.
    """

    def has_permission(self, request, view):
        # Permitir siempre los métodos seguros como GET
        if request.method in SAFE_METHODS:
            return True
        # Solo permitir escritura a administradores
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(BasePermission):
    """
    Permite editar/eliminar una subasta solo si el usuario es el propietario
    o es administrador. Cualquiera puede consultar (GET).
    """

    def has_object_permission(self, request, view, obj):
        # Permitir acceso de lectura a cualquier usuario (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Si el objeto es una subasta (Auction)
        if hasattr(obj, 'auctioneer'):
            return obj.auctioneer == request.user or request.user.is_staff        # Si el objeto es una puja (Bid)
        if hasattr(obj, 'bidder'):
            return str(obj.bidder) == str(request.user) or request.user.is_staff

        # Si el objeto es un comentario (Comment)
        if hasattr(obj, 'user'):
            return str(obj.user) == str(request.user.username) or request.user.is_staff

        # Por defecto, denegar el acceso
        return False


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Permitir siempre métodos seguros (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Para otros métodos, requerir login
        return request.user and request.user.is_authenticated
