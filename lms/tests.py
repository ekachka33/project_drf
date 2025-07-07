# lms/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson
from users.models import Subscription
from django.contrib.auth.models import Group

User = get_user_model()

class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        """
        Настройка тестовых данных перед каждым тестом.
        Создаем пользователей, группы, курсы, уроки и подписки.
        """
        # 1. Создаем тестовых пользователей
        self.user_owner = User.objects.create_user(
            email='owner@example.com',
            password='testpassword'
        )
        self.user_moderator = User.objects.create_user(
            email='moderator@example.com',
            password='testpassword'
        )
        self.user_another = User.objects.create_user(
            email='another@example.com',
            password='testpassword'
        )

        # 2. Создаем группу "Модераторы" и добавляем пользователя
        self.moderator_group, created = Group.objects.get_or_create(name='Модераторы')
        self.user_moderator.groups.add(self.moderator_group)

        # 3. Создаем тестовые курсы
        self.course_owner = Course.objects.create(
            title='Курс Владельца',
            description='Описание курса владельца',
            owner=self.user_owner
        )
        self.course_another = Course.objects.create(
            title='Другой Курс',
            description='Описание другого курса',
            owner=self.user_another
        )

        # 4. Создаем тестовые уроки
        self.lesson_owner = Lesson.objects.create(
            title='Урок Владельца',
            description='Описание урока владельца',
            video_link='https://www.youtube.com/watch?v=owner_lesson',
            course=self.course_owner,
            owner=self.user_owner
        )
        self.lesson_another = Lesson.objects.create(
            title='Другой Урок',
            description='Описание другого урока',
            video_link='https://www.youtube.com/watch?v=another_lesson',
            course=self.course_another,
            owner=self.user_another
        )

        # 5. Создаем тестовые подписки
        # Подписка user_owner на свой курс (хотя это не совсем логично, но для теста)
        Subscription.objects.create(user=self.user_owner, course=self.course_owner)
        # Подписка user_another на курс user_owner
        Subscription.objects.create(user=self.user_another, course=self.course_owner)


    # --- ТЕСТЫ CRUD ДЛЯ УРОКОВ ---

    def test_lesson_create(self):
        """
        Тест создания урока.
        Только владелец курса может создавать уроки.
        """
        self.client.force_authenticate(user=self.user_owner)
        data = {
            'title': 'Новый Урок',
            'description': 'Описание нового урока',
            'video_link': 'https://www.youtube.com/watch?v=new_lesson',
            'course': self.course_owner.id # Урок привязан к курсу владельца
        }
        response = self.client.post(reverse('lesson-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 3)
        self.assertEqual(Lesson.objects.get(title='Новый Урок').owner, self.user_owner)

    def test_lesson_create_forbidden_word(self):
        """
        Тест создания урока с запрещенным словом в названии.
        """
        self.client.force_authenticate(user=self.user_owner)
        data = {
            'title': 'Урок про фарфор', # Запрещенное слово
            'description': 'Описание урока',
            'video_link': 'https://www.youtube.com/watch?v=forbidden',
            'course': self.course_owner.id
        }
        response = self.client.post(reverse('lesson-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Слово \'фарфор\' запрещено в названии урока.', str(response.data))

    def test_lesson_list_owner(self):
        """
        Тест получения списка уроков владельцем.
        Владелец должен видеть только свои уроки.
        """
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Убедись, что пагинация работает, и мы получаем список в "results"
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], self.lesson_owner.title)

    def test_lesson_list_moderator(self):
        """
        Тест получения списка уроков модератором.
        Модератор должен видеть все уроки.
        """
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertIn(self.lesson_owner.title, [l['title'] for l in response.data['results']])
        self.assertIn(self.lesson_another.title, [l['title'] for l in response.data['results']])

    def test_lesson_list_unauthenticated(self):
        """
        Тест получения списка уроков неаутентифицированным пользователем.
        Должен получить 401 Unauthorized.
        """
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_retrieve_owner(self):
        """
        Тест получения деталей урока владельцем.
        """
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(reverse('lesson-detail', args=[self.lesson_owner.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson_owner.title)

    def test_lesson_retrieve_moderator(self):
        """
        Тест получения деталей урока модератором.
        """
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get(reverse('lesson-detail', args=[self.lesson_another.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson_another.title)

    def test_lesson_retrieve_another_user(self):
        """
        Тест получения деталей урока другим пользователем (не владельцем, не модератором).
        Должен получить 404 Not Found, так как урок не найден в его QuerySet.
        """
        self.client.force_authenticate(user=self.user_another)
        response = self.client.get(reverse('lesson-detail', args=[self.lesson_owner.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # <-- ИЗМЕНЕНО

    def test_lesson_update_owner(self):
        """
        Тест обновления урока владельцем.
        """
        self.client.force_authenticate(user=self.user_owner)
        updated_data = {'title': 'Обновленный Урок Владельца'}
        response = self.client.patch(reverse('lesson-detail', args=[self.lesson_owner.pk]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson_owner.refresh_from_db()
        self.assertEqual(self.lesson_owner.title, 'Обновленный Урок Владельца')

    def test_lesson_update_moderator(self):
        """
        Тест обновления урока модератором.
        Модератор может обновлять любой урок.
        """
        self.client.force_authenticate(user=self.user_moderator)
        updated_data = {'title': 'Обновленный Урок Модератором'}
        response = self.client.patch(reverse('lesson-detail', args=[self.lesson_another.pk]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson_another.refresh_from_db()
        self.assertEqual(self.lesson_another.title, 'Обновленный Урок Модератором')

    def test_lesson_update_another_user(self):
        """
        Тест обновления урока другим пользователем.
        Должен получить 404 Not Found, так как урок не найден в его QuerySet.
        """
        self.client.force_authenticate(user=self.user_another)
        updated_data = {'title': 'Попытка обновления'}
        response = self.client.patch(reverse('lesson-detail', args=[self.lesson_owner.pk]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # <-- ИЗМЕНЕНО

    def test_lesson_delete_owner(self):
        """
        Тест удаления урока владельцем.
        """
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.delete(reverse('lesson-detail', args=[self.lesson_owner.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_delete_moderator(self):
        """
        Тест удаления урока модератором.
        Модератор не может удалять уроки (если у них нет такого права по IsOwner).
        Сейчас ожидается 403, если модератор не является владельцем и IsModerator не дает права на удаление.
        """
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.delete(reverse('lesson-detail', args=[self.lesson_another.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_delete_another_user(self):
        """
        Тест удаления урока другим пользователем.
        Должен получить 404 Not Found, так как урок не найден в его QuerySet.
        """
        self.client.force_authenticate(user=self.user_another)
        response = self.client.delete(reverse('lesson-detail', args=[self.lesson_owner.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Lesson.objects.count(), 2)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        """
        Настройка тестовых данных для тестов подписок.
        """
        self.user_subscriber = User.objects.create_user(
            email='subscriber@example.com',
            password='testpassword'
        )
        self.user_owner = User.objects.create_user(
            email='owner@example.com',
            password='testpassword'
        )
        self.course = Course.objects.create(
            title='Тестовый Курс',
            description='Описание тестового курса',
            owner=self.user_owner
        )

    def test_subscribe_to_course(self):
        """
        Тест подписки на курс.
        """
        self.client.force_authenticate(user=self.user_subscriber)
        data = {'course': self.course.id}
        response = self.client.post(reverse('subscriptions'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user_subscriber, course=self.course).exists())
        self.assertEqual(response.data['message'], 'Подписка добавлена')


    def test_unsubscribe_from_course(self):
        """
        Тест отписки от курса.
        """
        Subscription.objects.create(user=self.user_subscriber, course=self.course)
        self.client.force_authenticate(user=self.user_subscriber)
        data = {'course': self.course.id}
        response = self.client.post(reverse('subscriptions'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user_subscriber, course=self.course).exists())
        self.assertEqual(response.data['message'], 'Подписка удалена')

    def test_subscribe_unauthenticated(self):
        """
        Тест подписки без аутентификации.
        """
        data = {'course': self.course.id}
        response = self.client.post(reverse('subscriptions'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_owner_to_own_course(self):
        """
        Тест подписки владельца на свой собственный курс.
        Должно быть возможно, если нет явного запрета.
        """
        self.client.force_authenticate(user=self.user_owner)
        data = {'course': self.course.id}
        response = self.client.post(reverse('subscriptions'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user_owner, course=self.course).exists())
        self.assertEqual(response.data['message'], 'Подписка добавлена')