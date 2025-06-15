"""
URL configuration for project_drf_new project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Убедитесь, что импортируются только ViewSet'ы, которые вы будете регистрировать через роутер
from lms.views import CourseViewSet, LessonViewSet
from users.views import PaymentViewSet, UserViewSet # Проверьте, что PaymentViewSet существует
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Создаем экземпляр DefaultRouter
router = DefaultRouter()
# Явно указываем basename для ясности и во избежание проблем
router.register(r'users', UserViewSet, basename='user') # Изменено: добавлен basename
router.register(r'courses', CourseViewSet, basename='course') # Можно поменять на 'course' или оставить 'courses'
router.register(r'lessons', LessonViewSet, basename='lesson') # Изменено: добавлен basename, можно поменять на 'lesson' или оставить 'lessons'
router.register(r'payments', PaymentViewSet, basename='payment') # Изменено: добавлен basename


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)), # <-- Оставляем только один include роутера
    # path('lms/', include(lms.urls)), # <-- ЭТУ СТРОКУ НУЖНО УДАЛИТЬ, так как LessonViewSet теперь через роутер
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)