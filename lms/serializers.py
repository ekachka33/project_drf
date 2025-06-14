from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.
    Преобразует объекты Course в формат JSON и обратно.
    """
    class Meta:
        model = Course
        fields = '__all__'  # Включаем все поля модели Course

class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    Преобразует объекты Lesson в формат JSON и обратно.
    """
    class Meta:
        model = Lesson
        fields = '__all__'  # Включаем все поля модели Lesson