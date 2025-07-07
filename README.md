LMS API Project

Этот проект представляет собой RESTful API для системы управления обучением (LMS), 
разработанной с использованием Django REST Framework. Система позволяет управлять курсами и уроками,
а также включает функционал подписки на обновления курсов.


Управление курсами: Полный CRUD для курсов.

Управление уроками: Полный CRUD для уроков.

Валидация ссылок: Проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.

Система подписок: Модель подписки на обновления курса для пользователя с полями «пользователь» (FK на модель пользователя) и «курс» (FK на модель курса). Реализован эндпоинт для установки и удаления подписки. При выборке данных по курсу пользователю присылается признак подписки текущего пользователя на курс.

Пагинация: Реализована для вывода всех уроков и курсов с настраиваемыми параметрами page_size, page_size_query_param, max_page_size.

Ролевой доступ: Обработаны варианты взаимодействия с контроллерами пользователей с разными правами доступа.

Управление пользователями: Создание и просмотр пользователей.

Управление платежами: Запись и просмотр информации о платежах.

Технологии
Python (3.12+)

Django (5.0+)

Django REST Framework

PostgreSQL

python-dotenv

Установка
Предварительные требования
Убедитесь, что у вас установлен Python 3.12+ и pip. Также потребуется установленный и запущенный сервер PostgreSQL.

Клонирование репозитория
Bash

git clone https://github.com/YourGitHubUsername/your_project_name.git # Замените на актуальные данные
cd your_project_name # Замените на имя вашей папки проекта
Настройка окружения
Создайте виртуальное окружение:

Bash

python -m venv .venv
Активируйте виртуальное окружение:

Для macOS/Linux:

Bash

source .venv/bin/activate
Для Windows:

Bash

.venv\Scripts\activate
Установите зависимости:

Bash

pip install -r requirements.txt
(Если файла requirements.txt нет, создайте его командой pip freeze > requirements.txt.)

Создайте файл .env:
Скопируйте содержимое файла .env.example в новый файл с именем .env в корневой директории проекта.
Откройте файл .env и заполните его своими реальными значениями (например, паролями для БД, секретным ключом Django и т.д.):

Ini, TOML

SECRET_KEY=your_django_secret_key_here
DEBUG=True # Установите False для продакшена

POSTGRES_DB=project_drf_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secret_password # Введите ваш реальный пароль
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# MEDIA_URL и MEDIA_ROOT (если используете локальное хранилище)
MEDIA_URL=/media/
MEDIA_ROOT=/path/to/your/project/media # Замените на фактический путь к вашей папке media


# .gitignore
.env
Убедитесь, что ваш settings.py настроен на чтение этих переменных из .env с помощью os.getenv().

Миграции базы данных
Bash

python manage.py migrate
Создание суперпользователя (для доступа к админ-панели)
Bash

python manage.py createsuperuser
Запуск сервера
Bash

python manage.py runserver
Теперь API будет доступен по адресу http://127.0.0.1:8000/.

Использование API
Для взаимодействия с API используйте такие инструменты, как Postman или Swagger UI (если интегрирован).

Аутентификация
Большинство эндпоинтов требуют аутентификации. Получите JWT токен, отправив POST запрос на /api/token/ с учетными данными пользователя.

Пример запроса на получение токена:

HTTP

POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
Используйте полученный access токен в заголовке Authorization: Bearer <YOUR_ACCESS_TOKEN> для аутентифицированных запросов.

Доступные эндпоинты
/users/ - Управление пользователями.

/courses/ - Управление курсами.

/lessons/ - Управление уроками.

/payments/ - Управление платежами.

/subscriptions/ - Эндпоинт для подписки/отписки на курс (используйте POST запрос).

/api/token/ - Получение JWT токена.

/api/token/refresh/ - Обновление JWT токена.

/admin/ - Панель администратора Django.

Тестирование
Для запуска тестов и проверки покрытия кода:

Bash

coverage run manage.py test lms users payments # Укажите все приложения, которые хотите тестировать
coverage report -m
Все тесты должны пройти успешно (OK).


