# users/views.py

# Стандартные импорты Django
from django.contrib.auth import get_user_model

# Импорты сторонних библиотек
import django_filters
import django_filters.rest_framework # Если не используется явно, можно убрать
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

# Импорты из текущего проекта/приложения
from .models import Payment # Убедись, что модель Payment существует и доступна
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter # Убедись, что users/filters.py существует и содержит PaymentFilter


# Инициализация модели пользователя
User = get_user_model()


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.
    Предоставляет операции CRUD, а также фильтрацию и сортировку.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # Используем DjangoFilterBackend для фильтрации и OrderingFilter для сортировки
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter # Применяем наш PaymentFilter
    ordering_fields = ['payment_date', 'payment_amount'] # Поля, по которым разрешена сортировка
    ordering = ['-payment_date'] # Сортировка по умолчанию: от новых платежей к старым


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.
    Предоставляет операции CRUD. Разрешения настраиваются динамически.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений в зависимости от текущего действия (action).
        - Для действия 'create' (регистрация) разрешен доступ всем (AllowAny).
        - Для всех остальных действий (просмотр, обновление, удаление) требуется аутентификация (IsAuthenticated).
        """
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]