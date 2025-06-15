# lms/validators.py

from rest_framework.serializers import ValidationError

def validate_youtube_link(value):
    """
    Валидатор для проверки, что ссылка на видео строго начинается с "youtube.com".
    """
    if not value:
        return

    allowed_prefix = "youtube.com"

    if not value.startswith(allowed_prefix):
        raise ValidationError(f"Разрешены ссылки только с началом '{allowed_prefix}'.")