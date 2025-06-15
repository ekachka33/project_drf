# users/views.py
import django_filters
from rest_framework import viewsets
from users.models import Payment
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter # Для сортировки, если не использовали OrderingFilter в PaymentFilter
import django_filters.rest_framework
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter) # Добавляем бэкенды фильтрации и сортировки
    filterset_class = PaymentFilter # Указываем наш PaymentFilter
    ordering_fields = ['payment_date', 'payment_amount']
    ordering = ['-payment_date'] # Сортировка по умолчанию (но filter.OrderingFilter переопределит ее, если передать параметр)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # Используем get_user_model() для получения User
    serializer_class = UserSerializer

    # Настройка разрешений в зависимости от действия (action)
    def get_permissions(self):
        if self.action == 'create': # Для регистрации (создания пользователя)
            self.permission_classes = [AllowAny]
        else: # Для просмотра, редактирования, удаления (т.е. для CRUD)
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

# Добавляем импорт User (если его нет)
from django.contrib.auth import get_user_model
User = get_user_model()