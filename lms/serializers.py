from rest_framework import serializers
from lms.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    Преобразует объекты Lesson в формат JSON и обратно.
    """
    class Meta:
        model = Lesson
        fields = '__all__'  # Включаем все поля модели Lesson


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True)
    """
    Сериализатор для модели Course.
    Преобразует объекты Course в формат JSON и обратно.
    """
    class Meta:
        model = Course
        fields = '__all__'  # Включаем все поля модели Course

    def get_lessons_count(self, obj):
        return obj.lessons.count()


