# lms/models.py

from django.db import models
from django.conf import settings  # <-- Убедитесь, что это импортировано


class Course(models.Model):
    # Если вы хотите использовать 'name' вместо 'title', это нормально.
    # Но для согласованности с предыдущими шагами и verbose_name
    # я рекомендую использовать 'title'.
    title = models.CharField(max_length=255, verbose_name='Название курса')  # Используйте 'title'

    preview = models.ImageField(
        upload_to='course_previews/',
        blank=True,  # Может быть пустым в формах
        null=True,  # Может быть NULL в базе данных
        verbose_name='Превью курса'
    )
    description = models.TextField(verbose_name='Описание курса')

    # Добавляем поле владельца для Задания 3
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Ссылка на вашу пользовательскую модель
        on_delete=models.SET_NULL,  # Если владелец удален, поле owner станет NULL
        null=True,  # Может быть NULL в базе данных
        blank=True,  # Может быть пустым в формах
        verbose_name='Владелец курса'
    )

    def __str__(self):
        return self.title  # Используйте title, если вы поменяли 'name' на 'title'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='lessons',  # Это уже было у вас, оставляем
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    title = models.CharField(max_length=255, verbose_name='Название урока')  # Используйте 'title'
    description = models.TextField(verbose_name='Описание урока')
    preview = models.ImageField(
        upload_to='lesson_previews/',
        blank=True,  # Может быть пустым в формах
        null=True,  # Может быть NULL в базе данных
        verbose_name='Превью урока'
    )
    video_link = models.URLField(
        blank=True,  # Может быть пустым в формах
        null=True,  # Может быть NULL в базе данных
        verbose_name='Ссылка на видео'
    )

    # Добавляем поле владельца для Задания 3
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Если владелец удален, поле owner станет NULL
        null=True,  # Может быть NULL в базе данных
        blank=True,  # Может быть пустым в формах
        verbose_name='Владелец урока'
    )

    def __str__(self):
        return self.title  # Используйте title, если вы поменяли 'name' на 'title'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'