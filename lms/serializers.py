# lms/serializers.py

from rest_framework import serializers
from lms.models import Course, Lesson
from .validators import validate_youtube_link # <-- Обязательно импортируйте здесь!

class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    """
    Сериализатор для модели Lesson.
    Преобразует объекты Lesson в формат JSON и обратно.
    """
    class Meta:
        model = Lesson
        fields = '__all__'  # Включаем все поля модели Lesson
        # Применяем валидатор к полю video_link
        extra_kwargs = {
            'video_link': {'validators': [validate_youtube_link]},
        }

    def validate(self, data):  # <-- Это валидатор для "фарфор"/"керамика"
        forbidden_words = ['фарфор', 'керамика']

        if 'title' in data and data['title']:
            title_lower = data['title'].lower()
            for word in forbidden_words:
                if word in title_lower:
                    raise serializers.ValidationError(
                        f"Слово '{word}' запрещено в названии урока."
                    )

        if 'description' in data and data['description']:
            description_lower = data['description'].lower()
            for word in forbidden_words:
                if word in description_lower:
                    raise serializers.ValidationError(
                        f"Слово '{word}' запрещено в описании урока."
                    )
        return data


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')

    lessons = LessonSerializer(many=True, read_only=True)
    """
    Сериализатор для модели Course.
    Преобразует объекты Course в формат JSON и обратно.
    """
    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()