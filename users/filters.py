# users/filters.py
import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    # Определяем кастомные фильтры здесь. Их имена должны соответствовать полям модели,
    # если ты хочешь, чтобы они работали с этими полями.
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Payment
        # В 'fields' перечисляем только те поля модели, для которых НЕ определены кастомные фильтры выше.
        # Если все нужные фильтры определены выше, этот список может быть пустым.
        # В твоем случае, если 'user' и 'created_at' обрабатываются кастомными фильтрами,
        # а других полей для стандартной фильтрации нет, оставляем пустым.
        fields = [] # Оставляем пустым, если все нужные поля определены как кастомные фильтры выше
        # Или, если у тебя есть другие поля в Payment (например, 'amount'), которые ты хочешь фильтровать стандартно:
        # fields = ['amount']