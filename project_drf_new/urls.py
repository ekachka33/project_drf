"""
URL configuration for project_drf_new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet
import lms.urls
from lms.views import CourseViewSet, LessonViewSet
from users.views import PaymentViewSet # Импортируем наш PaymentViewSet
from django.conf import settings
from django.conf.urls.static import static

# Создаем экземпляр DefaultRouter
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet) # Убедитесь, что LessonViewSet тоже зарегистрирован, если его нет
router.register(r'payments', PaymentViewSet) # <-- ДОБАВИТЬ ЭТО


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('lms/', include(lms.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Эта строка для статических файлов, но ее наличие не повредит
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
