from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import User


class Command(BaseCommand):
    help = 'Загружает тестовых пользователей и проекты'

    def handle(self, *args, **options):
        if User.objects.filter(email='admin@teamfinder.ru').exists():
            self.stdout.write('Данные уже загружены.')
            return

        admin = User.objects.create_superuser(
            email='admin@teamfinder.ru',
            password='admin12345',
            first_name='Админ',
            last_name='Системный',
        )

        users_data = [
            {
                'email': 'maria@example.com',
                'password': 'testpass123',
                'first_name': 'Мария',
                'last_name': 'Байбородина',
                'bio': 'Frontend-разработчик с опытом в React и Vue.js.',
                'phone': '+7 900 111-22-33',
                'github': 'https://github.com/maria-dev',
            },
            {
                'email': 'nikita@example.com',
                'password': 'testpass123',
                'first_name': 'Никита',
                'last_name': 'Воронин',
                'bio': 'Python Backend Developer. Специализируюсь на Django.',
                'phone': '+7 900 222-33-44',
                'github': 'https://github.com/nikita-dev',
            },
            {
                'email': 'alex@example.com',
                'password': 'testpass123',
                'first_name': 'Алексей',
                'last_name': 'Иванов',
                'bio': 'Full-stack разработчик и DevOps-инженер.',
                'phone': '+7 900 333-44-55',
                'github': 'https://github.com/alex-dev',
            },
        ]

        users = []
        for data in users_data:
            password = data.pop('password')
            user = User.objects.create_user(**data)
            user.set_password(password)
            user.save()
            users.append(user)

        projects_data = [
            {
                'title': 'Платформа для mental health поддержки MindSpace',
                'description': (
                    'Разрабатываем приложение для поддержки ментального здоровья. '
                    'Функционал: дневник эмоций с AI-анализом, медитации и практики.'
                ),
                'author': users[0],
            },
            {
                'title': 'Fitness трекер с геймификацией FitQuest',
                'description': (
                    'Мобильное приложение для отслеживания физической активности '
                    'с элементами игры и квестов.'
                ),
                'author': users[1],
            },
            {
                'title': 'Децентрализованная платформа для фрилансеров Web3Lance',
                'description': (
                    'Блокчейн-платформа для фрилансеров без посредников '
                    'с умными контрактами.'
                ),
                'author': users[2],
            },
            {
                'title': 'AI-ассистент для изучения языков LinguaBot',
                'description': (
                    'Чат-бот на базе ИИ для практики иностранных языков '
                    'с исправлением ошибок.'
                ),
                'author': users[1],
            },
            {
                'title': 'Экологический маркетплейс GreenChoice',
                'description': (
                    'Маркетплейс для продажи экологичных товаров '
                    'от локальных производителей.'
                ),
                'author': users[0],
            },
        ]

        projects = []
        for data in projects_data:
            project = Project.objects.create(**data)
            projects.append(project)

        projects[1].participants.add(users[0], users[2])
        projects[2].participants.add(users[1])
        projects[4].participants.add(users[1], users[2])

        projects[0].favorited_by.add(users[1])
        projects[1].favorited_by.add(users[0], users[2])
        projects[4].favorited_by.add(users[2])

        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены.'))
        self.stdout.write('Админ: admin@teamfinder.ru / admin12345')
        self.stdout.write('Пользователи: maria@example.com, nikita@example.com, alex@example.com / testpass123')
