# users/views.py
import django_filters
from rest_framework import viewsets
from users.models import Payment, Subscription
from .serializers import PaymentSerializer, UserSerializer
from .filters import PaymentFilter
from rest_framework.filters import OrderingFilter
import django_filters.rest_framework
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from lms.models import Course
from django.contrib.auth import get_user_model
User = get_user_model()


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date', 'payment_amount']
    ordering = ['-payment_date']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')

        if not course_id:
            return Response({"message": "ID курса не предоставлен."}, status=400)

        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=200)
