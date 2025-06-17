# users/management/commands/create_moderator_group.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Импортируем модели, для которых будут назначаться права.
# Убедись, что эти импорты соответствуют твоим моделям!
# Например, если у тебя пользовательская модель User в приложении users:
from users.models import User
# Если у тебя есть модели Course, Lesson, Payment:
from lms.models import Course, Lesson
from users.models import Payment # Или из другого приложения, если Payment не в users


class Command(BaseCommand):
    help = 'Создает группу "Модераторы" и назначает ей необходимые права доступа.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаем настройку группы "Модераторы"...'))

        # 1. Создаем или получаем группу "Модераторы"
        moderators_group, created = Group.objects.get_or_create(name='Модераторы')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модераторы" уже существует. Обновляем разрешения...'))

        # Список разрешений, которые мы хотим назначить модераторам
        # Каждое разрешение идентифицируется по 'codename' и 'content_type'
        permissions_to_add = []

        # Получаем ContentType для каждой модели, с которой модераторы должны работать
        # (Это позволяет получить разрешения, связанные с конкретной моделью)
        try:
            content_type_user = ContentType.objects.get_for_model(User)
            content_type_course = ContentType.objects.get_for_model(Course)
            content_type_lesson = ContentType.objects.get_for_model(Lesson)
            content_type_payment = ContentType.objects.get_for_model(Payment)
        except ContentType.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: Не удалось найти ContentType для одной из моделей. Убедитесь, что модели ({e}) импортированы и существуют."))
            self.stdout.write(self.style.WARNING("Пропускаем назначение разрешений для несуществующих моделей."))
            return # Выходим, если не можем найти ContentType

        # --- Назначаем разрешения ---
        # Модераторы могут просматривать, изменять и удалять *пользователей*
        permissions_to_add.extend([
            Permission.objects.get(codename='view_user', content_type=content_type_user),
            Permission.objects.get(codename='change_user', content_type=content_type_user),
            # Permission.objects.get(codename='delete_user', content_type=content_type_user), # Если модераторам можно удалять пользователей
        ])

        # Модераторы могут просматривать, изменять и удалять *курсы*
        permissions_to_add.extend([
            Permission.objects.get(codename='view_course', content_type=content_type_course),
            Permission.objects.get(codename='change_course', content_type=content_type_course),
            Permission.objects.get(codename='delete_course', content_type=content_type_course),
            # Permission.objects.get(codename='add_course', content_type=content_type_course), # Если модераторам можно создавать курсы
        ])

        # Модераторы могут просматривать, изменять и удалять *уроки*
        permissions_to_add.extend([
            Permission.objects.get(codename='view_lesson', content_type=content_type_lesson),
            Permission.objects.get(codename='change_lesson', content_type=content_type_lesson),
            Permission.objects.get(codename='delete_lesson', content_type=content_type_lesson),
            # Permission.objects.get(codename='add_lesson', content_type=content_type_lesson), # Если модераторам можно создавать уроки
        ])

        # Модераторы могут просматривать, изменять и удалять *платежи*
        permissions_to_add.extend([
            Permission.objects.get(codename='view_payment', content_type=content_type_payment),
            Permission.objects.get(codename='change_payment', content_type=content_type_payment),
            Permission.objects.get(codename='delete_payment', content_type=content_type_payment),
            # Permission.objects.get(codename='add_payment', content_type=content_type_payment), # Если модераторам можно создавать платежи
        ])


        # 2. Очищаем старые разрешения и назначаем новые
        # Это гарантирует, что у группы будут только те разрешения, которые мы явно перечислили
        moderators_group.permissions.set(permissions_to_add)

        self.stdout.write(self.style.SUCCESS(f'Разрешения для группы "{moderators_group.name}" успешно обновлены.'))
        self.stdout.write(self.style.SUCCESS('Настройка группы "Модераторы" завершена.'))