# users/permissions.py

from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Кастомный пермишен, который разрешает доступ только модераторам.
    Модераторы имеют доступ только к редактированию (PUT/PATCH) и просмотру (GET),
    но не к созданию (POST) или удалению (DELETE).
    """

    def has_permission(self, request, view):
        # Проверяем, является ли пользователь аутентифицированным
        if not request.user.is_authenticated:
            return False

        # Проверяем, находится ли пользователь в группе "Модераторы"
        if request.user.groups.filter(name='Модераторы').exists():
            # Модераторы могут просматривать (GET) и редактировать (PUT, PATCH)
            if view.action in ['retrieve', 'list', 'update', 'partial_update']:
                return True
            # Но не могут создавать (POST) или удалять (DELETE)
            elif view.action in ['create', 'destroy']:
                return False

        # Для других методов или если пользователь не модератор, используем другие пермишены
        return False # По умолчанию запрещаем, если не разрешено выше

    def has_object_permission(self, request, view, obj):
        # Разрешает модераторам просмотр и редактирование любых объектов (курсов/уроков)
        # Если это не модератор, то этот пермишен не применяется,
        # и будет использован другой (например, IsOwner)
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        return False # Если не модератор, то этот пермишен не дает разрешение

class IsOwner(permissions.BasePermission): # <-- Добавляем новый класс IsOwner
    """
    Кастомный пермишен, который разрешает доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение всегда разрешено, если это не POST (для POST нужно has_permission)
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True

        # Разрешение на запись разрешено только владельцу объекта
        # Предполагается, что объект имеет атрибут 'owner'
        return obj.owner == request.user

    def has_permission(self, request, view):
        # Для POST-запросов (создание), если пользователь аутентифицирован,
        # и он не модератор (т.к. модераторы не могут создавать),
        # мы разрешаем ему создавать объект.
        if request.method == 'POST':
            return request.user.is_authenticated and not request.user.groups.filter(name='Модераторы').exists()
        # Для других методов has_object_permission будет проверять владение
        return True # Изначально разрешаем, потом сужаем в has_object_permission