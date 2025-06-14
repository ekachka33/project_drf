# users/views.py
import django_filters
from rest_framework import viewsets
from users.models import Payment
from .serializers import PaymentSerializer # Вам нужно будет создать PaymentSerializer
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter # Для сортировки, если не использовали OrderingFilter в PaymentFilter

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter) # Добавляем бэкенды фильтрации и сортировки
    filterset_class = PaymentFilter # Указываем наш PaymentFilter
    ordering_fields = ['payment_date', 'payment_amount']
    ordering = ['-payment_date'] # Сортировка по умолчанию (но filter.OrderingFilter переопределит ее, если передать параметр)