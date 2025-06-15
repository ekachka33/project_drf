# users/serializers.py

from rest_framework import serializers
from rest_framework.exceptions import ValidationError # Оставьте, если хотите использовать для других проверок
from django.contrib.auth import get_user_model

# Убедитесь, что эти импорты верны, исходя из вашей структуры проекта
from users.models import Payment # Если Payment находится в users/models.py
from lms.models import Course, Lesson # Если Course и Lesson нужны здесь и находятся в lms/models.py


# Получаем вашу кастомную модель User, которую вы определили в users/models.py
User = get_user_model()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # УДАЛИТЕ 'username' из списка fields!
        # Добавьте другие поля, если они должны быть доступны для создания/отображения,
        # например 'phone', 'city', 'avatar'
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'password') # 'id' можно вернуть для отображения
        extra_kwargs = {
            'password': {'write_only': True}, # Пароль только для записи
            # 'email': {'required': True} # email уже является USERNAME_FIELD, поэтому по умолчанию требуется
        }

    def create(self, validated_data):
        # *** ОТЛАДОЧНЫЙ ВЫВОД: Проверим, что находится в validated_data ***
        print(f"\n--- Отладка в UserSerializer.create ---")
        print(f"Полученные validated_data: {validated_data}")
        print(f"Есть ли 'email' в validated_data? {'email' in validated_data}")
        print(f"Значение 'email' (если есть): {validated_data.get('email', 'N/A')}")
        print(f"---------------------------------------\n")

        # Теперь вызываем create_user с email, а не username
        # Ваша модель User ожидает email как основной аргумент
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            # Передаем другие поля, если они есть в validated_data и вы хотите их сохранить при создании
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