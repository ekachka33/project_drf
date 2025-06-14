from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Payment, User


class PaymentAdmin(admin.ModelAdmin):
    # Добавляем list_display для отображения нужных полей в списке
    list_display = (
        'user',
        'payment_date',
        'paid_course',
        'paid_lesson',
        'payment_amount',
        'payment_method'
    )


admin.site.register(Payment, PaymentAdmin)

admin.site.register(User)

