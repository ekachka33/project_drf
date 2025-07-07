import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = [
            'paid_course',  # Поле из модели Payment
            'paid_lesson',  # Поле из модели Payment
            'payment_method',  # Поле из модели Payment
            'payment_date',  # Поле из модели Payment (для точного совпадения или других lookup_expr)
        ]