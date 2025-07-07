# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # *** ОТЛАДОЧНЫЙ ВЫВОД: Проверим, что находится в validated_data ***
        print(f"\n--- Отладка в UserSerializer.create ---")
        print(f"Полученные validated_data: {validated_data}")
        print(f"Есть ли 'email' в validated_data? {'email' in validated_data}")
        print(f"Значение 'email' (если есть): {validated_data.get('email', 'N/A')}")
        print(f"---------------------------------------\n")

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            city=validated_data.get('city'),
            avatar=validated_data.get('avatar'),
        )
        return user

    def update(self, instance, validated_data):
        # Обновление пароля, если он передан
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        # Обновление других полей
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.city = validated_data.get('city', instance.city)
        instance.avatar = validated_data.get('avatar', instance.avatar)

        # Сохраняем экземпляр после всех изменений
        instance.save()
        return instance