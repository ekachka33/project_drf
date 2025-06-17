from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import PaymentViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]