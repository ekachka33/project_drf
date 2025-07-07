from django.contrib import admin
from .models import Course, Lesson

# Register your models here.

# Регистрируем модель Course
admin.site.register(Course)

# Регистрируем модель Lesson
admin.site.register(Lesson)