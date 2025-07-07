# lms/validators.py

from rest_framework.serializers import ValidationError
from rest_framework.serializers import ValidationError
from urllib.parse import urlparse

def validate_youtube_link(value):
    """
    Валидатор для проверки, что ссылка на видео относится к googleusercontent.com
    или google.com/youtube.
    """
    if not value:
        return

    # Разрешенные домены
    allowed_domain_parts = [
        "googleusercontent.com",
        "youtube.com"
    ]

    try:
        parsed_url = urlparse(value)
        link_domain = parsed_url.netloc

        is_allowed = False
        for domain_part in allowed_domain_parts:
            if domain_part in link_domain:
                is_allowed = True
                break


        if not is_allowed:
            raise ValidationError(
                "Разрешены ссылки только с доменов 'googleusercontent.com' или 'youtube.com'."
            )

    except ValueError:
        raise ValidationError("Некорректный формат URL.")