from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset для модели Course.
    Предоставляет операции CRUD (Create, Retrieve, Update, Destroy, List).
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# --- Generic-классы для модели Lesson ---

class LessonListAPIView(generics.ListAPIView):
    """
    APIView для получения списка всех уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    APIView для получения одного урока по его ID.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonCreateAPIView(generics.CreateAPIView):
    """
    APIView для создания нового урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    APIView для обновления существующего урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    APIView для удаления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonViewSet(viewsets.ModelViewSet): # <-- ЭТОТ КЛАСС ДОЛЖЕН СУЩЕСТВОВАТЬ
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer