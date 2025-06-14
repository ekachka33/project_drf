# users/serializers.py

from rest_framework import serializers
from users.models import Payment, User # Импортируйте User, если хотите его сериализовать
from lms.models import Course, Lesson # Импортируйте, если хотите детали курсов/уроков


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

